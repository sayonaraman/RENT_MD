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
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
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
MIN_PRICE_EUR = 450
MAX_PRICE_EUR = 700
MAX_DISTANCE_KM = 3
STROLLER_WALKING_SPEED_KMH = 3.5
GEOCODE_DELAY_SECONDS = 1.1
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
ROUTE_URL = "https://valhalla1.openstreetmap.de/sources_to_targets"
USER_AGENT = "RentalWatcher/1.0 (+personal apartment search)"

DESTINATIONS = (
    {
        "key": "malinki",
        "name": "«Малинок»",
        "address": "Strada Studenților 3/10, Chișinău, Moldova",
        "latitude": 47.0623155,
        "longitude": 28.8638136,
    },
    {
        "key": "kindergarten-118",
        "name": "садика №118",
        "address": "bd. Moscova 14/2, Chișinău, Moldova",
        "latitude": 47.0533222,
        "longitude": 28.8667214,
    },
)

STATE_DIR = Path(__file__).parent / "state"
SEEN_FILE = STATE_DIR / "seen.json"
FILTERED_FILE = STATE_DIR / "filtered_ids.json"
GEOCODE_CACHE_FILE = STATE_DIR / "geocode_cache.json"

DISTRICT_RE = re.compile(r"рышкан|рышкановк|rîșcan|râșcan|riscan|ryscan", re.IGNORECASE)
TWO_ROOM_RE = re.compile(
    r"\b(?:2\s*[-–—]?\s*комн|2\s*к\b|двух[-\s]?комн|двушк|2\s*(?:camer[aeăi]|cam\b|odaie|odai))",
    re.IGNORECASE,
)
ONE_ROOM_RE = re.compile(
    r"\b(?:1\s*[-–—]?\s*комн|1\s*к\b|одно[-\s]?комн|однушк|1\s*(?:camer[aeăi]|cam\b|odaie|odai))",
    re.IGNORECASE,
)
LIVING_RE = re.compile(r"\b(?:ливинг|living|livingroom|salon)\b", re.IGNORECASE)
PRICE_RE = re.compile(
    r"(?:(?:€|eur|euro|евро)\s*(\d{2,5})|(\d{2,5})\s*(?:€|eur|euro|евро))",
    re.IGNORECASE,
)
ADDRESS_MARKER_RE = re.compile(r"^\s*📍\s*(.+?)\s*$")


def extract_price(text: str) -> int | None:
    prices = [int(a or b) for a, b in PRICE_RE.findall(text)]
    prices = [price for price in prices if 50 <= price <= 10000]
    return min(prices) if prices else None


def extract_address(text: str) -> str | None:
    for line in text.splitlines():
        match = ADDRESS_MARKER_RE.match(line)
        if not match:
            continue
        address = match.group(1).strip(" ,.")
        address = re.sub(
            r"^(?:рышкановк[а-я]*|rîșcani|râșcani|riscani)\s*,?\s*",
            "",
            address,
            flags=re.IGNORECASE,
        )
        address = re.sub(r"^str\.\s*", "Strada ", address, flags=re.IGNORECASE)
        address = re.sub(r"^str-la\s+", "Strada ", address, flags=re.IGNORECASE)
        address = re.sub(r"^bd\.\s*", "Bulevardul ", address, flags=re.IGNORECASE)
        address = re.sub(r"^ул\.\s*", "Strada ", address, flags=re.IGNORECASE)
        return address.strip(" ,.") or None
    return None


def parse_listing(text: str) -> dict | None:
    if not text.strip() or not DISTRICT_RE.search(text):
        return None
    is_two_room = bool(TWO_ROOM_RE.search(text))
    is_one_room_living = bool(ONE_ROOM_RE.search(text) and LIVING_RE.search(text))
    if not (is_two_room or is_one_room_living):
        return None
    price_eur = extract_price(text)
    if price_eur is None or not MIN_PRICE_EUR <= price_eur <= MAX_PRICE_EUR:
        return None
    address = extract_address(text)
    if not address:
        return None
    return {
        "price_eur": price_eur,
        "rooms": 2 if is_two_room else 1,
        "living": is_one_room_living,
        "address": address,
    }


def matches(text: str) -> bool:
    return parse_listing(text) is not None


def _load_json_map(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text())
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _save_json_map(path: Path, data: dict) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True))
    temporary.replace(path)


def _fetch_json(url: str) -> object:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _exact_geocode_result(results: object, house_number: str) -> dict | None:
    if not isinstance(results, list):
        return None
    pattern = re.compile(rf"(?:^|,\s*){re.escape(house_number)}(?:,|\s|$)", re.IGNORECASE)
    return next(
        (
            result for result in results
            if isinstance(result, dict)
            and pattern.search(str(result.get("display_name", "")))
            and result.get("addresstype") in {"building", "house", "place"}
        ),
        None,
    )


class LocationResolver:
    def __init__(self) -> None:
        self.cache = _load_json_map(GEOCODE_CACHE_FILE)
        self.last_geocode_at = 0.0

    async def geocode(self, address: str) -> tuple[float, float] | None:
        cached = self.cache.get(address)
        if isinstance(cached, list) and len(cached) == 2:
            return float(cached[0]), float(cached[1])

        house_match = re.search(r"(\d+(?:/\d+)?)\s*$", address)
        if not house_match:
            return None
        wait_seconds = GEOCODE_DELAY_SECONDS - (time.monotonic() - self.last_geocode_at)
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)
        query = urllib.parse.urlencode({
            "q": f"{address}, Chișinău, Moldova",
            "format": "jsonv2",
            "limit": "5",
        })
        results = await asyncio.to_thread(_fetch_json, f"{GEOCODE_URL}?{query}")
        self.last_geocode_at = time.monotonic()
        exact = _exact_geocode_result(results, house_match.group(1))
        if exact is None:
            return None
        coordinates = float(exact["lat"]), float(exact["lon"])
        self.cache[address] = list(coordinates)
        _save_json_map(GEOCODE_CACHE_FILE, self.cache)
        return coordinates

    async def routes(self, latitude: float, longitude: float) -> list[dict]:
        payload = {
            "sources": [{"lat": latitude, "lon": longitude}],
            "targets": [
                {"lat": destination["latitude"], "lon": destination["longitude"]}
                for destination in DESTINATIONS
            ],
            "costing": "pedestrian",
            "units": "kilometers",
        }
        query = urllib.parse.urlencode({
            "json": json.dumps(payload, separators=(",", ":")),
        })
        result = await asyncio.to_thread(_fetch_json, f"{ROUTE_URL}?{query}")
        matrix = result.get("sources_to_targets") if isinstance(result, dict) else None
        if not isinstance(matrix, list) or not matrix or not isinstance(matrix[0], list):
            raise RuntimeError("walking route API returned no matrix")
        routes = []
        for destination, route in zip(DESTINATIONS, matrix[0]):
            distance = route.get("distance") if isinstance(route, dict) else None
            distance_km = float(distance) if distance is not None else None
            routes.append({
                **destination,
                "distance_km": distance_km,
                "minutes_with_stroller": (
                    max(1, math.ceil((distance_km / STROLLER_WALKING_SPEED_KMH) * 60))
                    if distance_km is not None else None
                ),
            })
        return routes

    async def enrich(self, listing: dict) -> dict | None:
        coordinates = await self.geocode(listing["address"])
        if coordinates is None:
            return None
        routes = await self.routes(*coordinates)
        primary = next((route for route in routes if route["key"] == "malinki"), None)
        if primary is None or primary["distance_km"] is None:
            return None
        return {
            **listing,
            "latitude": coordinates[0],
            "longitude": coordinates[1],
            "walking_routes": routes,
            "eligible": primary["distance_km"] <= MAX_DISTANCE_KM,
        }


def format_route_note(listing: dict) -> str:
    lines = [f"Пешком от {listing['address']}:"]
    for route in listing["walking_routes"]:
        if route["distance_km"] is None:
            lines.append(f"• До {route['name']}: маршрут не определён")
        else:
            lines.append(
                f"• До {route['name']}: {route['distance_km']:.1f} км, "
                f"около {route['minutes_with_stroller']} мин с ребёнком и коляской"
            )
    return "\n".join(lines)


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
        resolver = LocationResolver()

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
        route_errors = 0
        new_filtered = 0
        for batch in ordered:
            text = "\n".join((m.message or "") for m in batch if m.message)
            listing = parse_listing(text)
            if listing is None:
                skipped_filter += 1
                for m in batch:
                    filtered_ids.add(m.id)
                new_filtered += len(batch)
                continue
            h = content_hash(text)
            if h in seen:
                skipped_dup += 1
                continue
            try:
                listing = await resolver.enrich(listing)
            except Exception as e:
                route_errors += 1
                print(f"route fail id={batch[0].id}: {e}", file=sys.stderr, flush=True)
                continue
            if listing is None or not listing["eligible"]:
                skipped_filter += 1
                for m in batch:
                    filtered_ids.add(m.id)
                new_filtered += len(batch)
                continue
            if args.dry_run:
                seen.add(h)
                print(format_route_note(listing), flush=True)
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
                try:
                    await client.send_message(
                        TARGET_CHAT,
                        format_route_note(listing),
                        reply_to=TARGET_TOPIC,
                        link_preview=False,
                    )
                except Exception as e:
                    print(f"route note fail id={batch[0].id}: {e}", file=sys.stderr, flush=True)
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
              f"отбраковано фильтром/маршрутом: {skipped_filter} (+{new_filtered} id в БД), "
              f"ошибок маршрута: {route_errors}, дубли пропущены: {skipped_dup} | "
              f"итого: seen={len(seen)}, filtered_ids={len(filtered_ids)}")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
