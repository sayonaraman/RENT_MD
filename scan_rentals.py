"""Сканер канала аренды: фильтр по району/комнатам/цене, форвард в тему группы.

БД:
  state/seen.json         — хеши контента уже отправленных (дедуп форвардов)
  state/filtered_ids.json — id источника, не прошедшие фильтр (повторно не разбираем)

Флаги:
  --dry-run   ничего не шлёт, только заполняет seen.json
  --reset     перед сканом чистит тему 17 в целевой группе и обнуляет state/*.json
"""
import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.helpers import generate_random_long
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ForwardMessagesRequest

SOURCE_CHAT = -1001662737751
TARGET_CHAT = -1003168733101
TARGET_TOPIC = 17
DAYS = 5
MAX_PRICE_EUR = 800

STATE_DIR = Path(__file__).parent / "state"
SEEN_FILE = STATE_DIR / "seen.json"
FILTERED_FILE = STATE_DIR / "filtered_ids.json"

DISTRICT_RE = re.compile(
    r"рышкан|рышкановк|rîșcan|râșcan|riscan|ryscan|чекан|ciocan|checani|cecan",
    re.IGNORECASE,
)

ROOMS_RES = [
    re.compile(r"\b([123])\s*[-–—]?\s*комн", re.IGNORECASE),
    re.compile(r"\b([123])\s*к\b", re.IGNORECASE),
    re.compile(r"\b(одно|двух|трех|трёх)[-\s]?комн", re.IGNORECASE),
    re.compile(r"\b(однушк|двушк|трешк|трёшк)", re.IGNORECASE),
    re.compile(r"\b([123])\s*(?:camer[aeăi]|cam\b|odaie|odai)", re.IGNORECASE),
]

PRICE_RE = re.compile(
    r"(?:(?:€|eur|euro|евро)\s*(\d{2,5})|(\d{2,5})\s*(?:€|eur|euro|евро))",
    re.IGNORECASE,
)


def has_district(text: str) -> bool:
    return bool(DISTRICT_RE.search(text))


def has_rooms(text: str) -> bool:
    return any(r.search(text) for r in ROOMS_RES)


def price_ok(text: str) -> bool:
    prices = [int(a or b) for a, b in PRICE_RE.findall(text)]
    prices = [p for p in prices if 50 <= p <= 10000]
    return bool(prices) and min(prices) <= MAX_PRICE_EUR


def matches(text: str) -> bool:
    return bool(text.strip()) and has_district(text) and has_rooms(text) and price_ok(text)


_NON_WORD = re.compile(r"[^\w]+", re.UNICODE)


def content_hash(text: str) -> str:
    norm = unicodedata.normalize("NFKC", text).lower()
    norm = _NON_WORD.sub(" ", norm).strip()
    norm = re.sub(r"\s+", " ", norm)[:400]
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]


def _load_set(path: Path) -> set:
    if path.is_file():
        try:
            return set(json.loads(path.read_text()))
        except Exception:
            return set()
    return set()


def _save_set(path: Path, data: set) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(sorted(data), indent=0))


async def purge_topic(client: TelegramClient) -> int:
    ids = []
    async for m in client.iter_messages(TARGET_CHAT, reply_to=TARGET_TOPIC):
        if m.id == TARGET_TOPIC:
            continue
        ids.append(m.id)
    deleted = 0
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        try:
            await client.delete_messages(TARGET_CHAT, batch)
            deleted += len(batch)
        except Exception as e:
            print(f"purge fail batch {i}: {e}", file=sys.stderr, flush=True)
    return deleted


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Только заполнить seen.json по текущим совпадениям, ничего не слать")
    parser.add_argument("--reset", action="store_true",
                        help="Очистить тему и обнулить state/*.json перед сканом")
    args = parser.parse_args()

    load_dotenv()
    if not all(os.environ.get(k) for k in ("TELEGRAM_API_ID", "TELEGRAM_API_HASH", "TELEGRAM_SESSION")):
        print("В .env нет TELEGRAM_*. Запусти «Настроить авторизацию.command».", file=sys.stderr)
        return 1

    api_id = int(os.environ["TELEGRAM_API_ID"])
    api_hash = os.environ["TELEGRAM_API_HASH"]
    session = os.environ["TELEGRAM_SESSION"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)

    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        if args.reset and not args.dry_run:
            print("=== очищаю тему ===", flush=True)
            removed = await purge_topic(client)
            print(f"удалено из темы: {removed}", flush=True)
            if SEEN_FILE.exists():
                SEEN_FILE.unlink()
            if FILTERED_FILE.exists():
                FILTERED_FILE.unlink()
            print("state/*.json сброшены", flush=True)

        seen = _load_set(SEEN_FILE)
        filtered_ids = _load_set(FILTERED_FILE)

        groups: "OrderedDict[int, list]" = OrderedDict()
        scanned = 0
        skipped_known = 0
        async for msg in client.iter_messages(SOURCE_CHAT):
            if msg.date < cutoff:
                break
            scanned += 1
            if msg.id in filtered_ids:
                skipped_known += 1
                continue
            key = msg.grouped_id or msg.id
            groups.setdefault(key, []).append(msg)

        ordered = list(groups.values())
        ordered.reverse()

        forwarded = 0
        skipped_filter = 0
        skipped_dup = 0
        new_filtered = 0
        for batch in ordered:
            text = "\n".join((m.message or "") for m in batch if m.message)
            if not matches(text):
                skipped_filter += 1
                for m in batch:
                    filtered_ids.add(m.id)
                new_filtered += len(batch)
                continue
            h = content_hash(text)
            if h in seen:
                skipped_dup += 1
                continue
            if args.dry_run:
                seen.add(h)
                continue
            ids = [m.id for m in sorted(batch, key=lambda m: m.id)]
            try:
                await client(ForwardMessagesRequest(
                    from_peer=SOURCE_CHAT,
                    id=ids,
                    random_id=[generate_random_long() for _ in ids],
                    to_peer=TARGET_CHAT,
                    top_msg_id=TARGET_TOPIC,
                ))
                forwarded += 1
                seen.add(h)
                _save_set(SEEN_FILE, seen)
                first = batch[0]
                preview = (first.message or "").strip().replace("\n", " ")[:80]
                print(f"→ {first.date:%Y-%m-%d %H:%M} id={first.id} | {preview}", flush=True)
            except Exception as e:
                print(f"fail id={batch[0].id}: {e}", file=sys.stderr, flush=True)

        _save_set(SEEN_FILE, seen)
        _save_set(FILTERED_FILE, filtered_ids)

        mode = "DRY-RUN" if args.dry_run else ("RESET+LIVE" if args.reset else "LIVE")
        print(f"\n[{mode}] просмотрено: {scanned}, пропущено по БД: {skipped_known}, "
              f"групп: {len(groups)}, переслано: {forwarded}, "
              f"отбраковано фильтром: {skipped_filter} (+{new_filtered} id в БД), "
              f"дубли пропущены: {skipped_dup} | "
              f"итого: seen={len(seen)}, filtered_ids={len(filtered_ids)}")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
