"""Import filtered Telegram rental posts into Postgres/Neon.

Secrets are read from environment variables only:
  TELEGRAM_API_ID / TELEGRAM_API_HASH / TELEGRAM_SESSION from .env
  NEON_DATABASE_URL or DATABASE_URL from .env.neon / shell env
"""
import argparse
import asyncio
import json
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb
from telethon import TelegramClient
from telethon.sessions import StringSession

from scan_rentals import (
    PRICE_RE,
    ROOMS_RES,
    SOURCE_CHAT,
    content_hash,
    matches,
)

ROOM_WORDS = {
    "одно": 1,
    "однушк": 1,
    "двух": 2,
    "двушк": 2,
    "трех": 3,
    "трёх": 3,
    "трешк": 3,
    "трёшк": 3,
}

ADDRESS_RE = re.compile(
    r"(?:str\.|ул\.|bd\.|бул\.|bulevard(?:ul)?|street)\s*[^,\n]{3,80}",
    re.IGNORECASE,
)


def detect_price(text: str) -> int | None:
    prices = [int(a or b) for a, b in PRICE_RE.findall(text)]
    prices = [price for price in prices if 50 <= price <= 10000]
    return min(prices) if prices else None


def detect_rooms(text: str) -> int | None:
    for pattern in ROOMS_RES:
        match = pattern.search(text)
        if not match:
            continue
        value = match.group(1).lower()
        if value.isdigit():
            return int(value)
        for word, rooms in ROOM_WORDS.items():
            if value.startswith(word):
                return rooms
    return None


def detect_district(text: str) -> str | None:
    lowered = text.lower()
    if re.search(r"чекан|чокан|ciocan|checani|cecan", lowered):
        return "Чокана"
    if re.search(r"рышкан|rîșcan|râșcan|riscan|ryscan", lowered):
        return "Рышкановка"
    return None


def detect_address(text: str) -> str | None:
    match = ADDRESS_RE.search(text)
    if not match:
        return None
    return re.sub(r"\s+", " ", match.group(0)).strip(" .,")


def detect_status(text: str) -> str:
    lowered = text.lower()
    if re.search(r"бронь|заброн|rezerv|reserved", lowered):
        return "reserved"
    return "active"


def media_kind(message) -> str | None:
    if getattr(message, "photo", None):
        return "photo"
    document = getattr(message, "document", None)
    if document:
        mime = getattr(document, "mime_type", "") or ""
        if mime.startswith("video/"):
            return "video"
        if mime.startswith("image/"):
            return "image"
        return "document"
    if getattr(message, "media", None):
        return type(message.media).__name__
    return None


def bool_match(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE))


def listing_from_batch(batch: list) -> dict:
    ordered = sorted(batch, key=lambda message: message.id)
    text = "\n".join((message.message or "") for message in ordered if message.message).strip()
    media = [
        {
            "source_message_id": message.id,
            "kind": kind,
        }
        for message in ordered
        for kind in [media_kind(message)]
        if kind
    ]
    first = ordered[0]
    return {
        "source_chat_id": SOURCE_CHAT,
        "source_group_id": str(first.grouped_id or first.id),
        "source_message_ids": [message.id for message in ordered],
        "first_message_id": first.id,
        "posted_at": first.date,
        "raw_text": text,
        "content_hash": content_hash(text),
        "district": detect_district(text),
        "rooms": detect_rooms(text),
        "price_eur": detect_price(text),
        "status": detect_status(text),
        "address": detect_address(text),
        "has_pets": bool_match(text, r"животн|питом|pet|animale"),
        "allows_kids": bool_match(text, r"дет|copii|kids"),
        "is_new_build": bool_match(text, r"новостр|bloc nou|new build"),
        "has_video": any(item["kind"] == "video" for item in media) or bool_match(text, r"видео|video"),
        "media": media,
    }


def create_schema(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            create table if not exists telegram_listings (
              id bigserial primary key,
              source_chat_id bigint not null,
              source_group_id text not null unique,
              source_message_ids bigint[] not null,
              first_message_id bigint not null,
              posted_at timestamptz not null,
              raw_text text not null,
              content_hash text not null unique,
              district text,
              rooms integer,
              price_eur integer,
              status text not null default 'active',
              address text,
              has_pets boolean not null default false,
              allows_kids boolean not null default false,
              is_new_build boolean not null default false,
              has_video boolean not null default false,
              media_count integer not null default 0,
              source_payload jsonb not null default '{}'::jsonb,
              created_at timestamptz not null default now(),
              updated_at timestamptz not null default now()
            );
            """
        )
        cur.execute(
            """
            create table if not exists telegram_listing_media (
              id bigserial primary key,
              listing_id bigint not null references telegram_listings(id) on delete cascade,
              source_message_id bigint not null,
              kind text not null,
              created_at timestamptz not null default now(),
              unique (listing_id, source_message_id, kind)
            );
            """
        )
        cur.execute("create index if not exists idx_telegram_listings_posted_at on telegram_listings (posted_at desc);")
        cur.execute("create index if not exists idx_telegram_listings_filters on telegram_listings (district, rooms, price_eur);")
    conn.commit()


def upsert_listing(conn: psycopg.Connection, listing: dict) -> int:
    payload = {
        "media": listing["media"],
        "imported_at": datetime.now(timezone.utc).isoformat(),
    }
    with conn.cursor() as cur:
        cur.execute(
            """
            insert into telegram_listings (
              source_chat_id, source_group_id, source_message_ids, first_message_id,
              posted_at, raw_text, content_hash, district, rooms, price_eur, status,
              address, has_pets, allows_kids, is_new_build, has_video, media_count,
              source_payload, updated_at
            )
            values (
              %(source_chat_id)s, %(source_group_id)s, %(source_message_ids)s, %(first_message_id)s,
              %(posted_at)s, %(raw_text)s, %(content_hash)s, %(district)s, %(rooms)s, %(price_eur)s,
              %(status)s, %(address)s, %(has_pets)s, %(allows_kids)s, %(is_new_build)s,
              %(has_video)s, %(media_count)s, %(source_payload)s, now()
            )
            on conflict (source_group_id) do update set
              source_message_ids = excluded.source_message_ids,
              raw_text = excluded.raw_text,
              content_hash = excluded.content_hash,
              district = excluded.district,
              rooms = excluded.rooms,
              price_eur = excluded.price_eur,
              status = excluded.status,
              address = excluded.address,
              has_pets = excluded.has_pets,
              allows_kids = excluded.allows_kids,
              is_new_build = excluded.is_new_build,
              has_video = excluded.has_video,
              media_count = excluded.media_count,
              source_payload = excluded.source_payload,
              updated_at = now()
            returning id;
            """,
            {
                **listing,
                "media_count": len(listing["media"]),
                "source_payload": Jsonb(payload),
            },
        )
        listing_id = cur.fetchone()[0]
        cur.execute("delete from telegram_listing_media where listing_id = %s;", (listing_id,))
        cur.executemany(
            """
            insert into telegram_listing_media (listing_id, source_message_id, kind)
            values (%s, %s, %s)
            on conflict do nothing;
            """,
            [(listing_id, item["source_message_id"], item["kind"]) for item in listing["media"]],
        )
    conn.commit()
    return listing_id


async def collect_listings(limit: int, days: int, scan_limit: int | None) -> tuple[list[dict], int]:
    load_dotenv()
    required = ("TELEGRAM_API_ID", "TELEGRAM_API_HASH", "TELEGRAM_SESSION")
    if not all(os.environ.get(key) for key in required):
        raise RuntimeError("Missing TELEGRAM_* credentials in .env")

    api_id = int(os.environ["TELEGRAM_API_ID"])
    api_hash = os.environ["TELEGRAM_API_HASH"]
    session = os.environ["TELEGRAM_SESSION"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    groups: "OrderedDict[int, list]" = OrderedDict()
    scanned = 0
    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        async for message in client.iter_messages(SOURCE_CHAT):
            if message.date < cutoff:
                break
            scanned += 1
            key = message.grouped_id or message.id
            groups.setdefault(key, []).append(message)
            if scan_limit and scanned >= scan_limit:
                break

    listings = []
    seen_hashes = set()
    for batch in groups.values():
        text = "\n".join((message.message or "") for message in batch if message.message)
        if not matches(text):
            continue
        listing = listing_from_batch(batch)
        if listing["content_hash"] in seen_hashes:
            continue
        seen_hashes.add(listing["content_hash"])
        listings.append(listing)
        if len(listings) >= limit:
            break
    return listings, scanned


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--days", type=int, default=120)
    parser.add_argument("--scan-limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    load_dotenv(".env.neon")
    database_url = os.environ.get("NEON_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if not database_url and not args.dry_run:
        print("No NEON_DATABASE_URL or DATABASE_URL found.", file=sys.stderr)
        return 1

    listings, scanned = await collect_listings(args.limit, args.days, args.scan_limit)
    print(f"scanned_messages={scanned} matched_listings={len(listings)}")
    if args.dry_run:
        for item in listings:
            preview = item["raw_text"].replace("\n", " ")[:100]
            print(f"- id={item['first_message_id']} price={item['price_eur']} rooms={item['rooms']} district={item['district']} | {preview}")
        return 0

    with psycopg.connect(database_url) as conn:
        create_schema(conn)
        ids = [upsert_listing(conn, item) for item in listings]
        with conn.cursor() as cur:
            cur.execute("select count(*) from telegram_listings;")
            total = cur.fetchone()[0]
    print(f"upserted={len(ids)} db_ids={ids} total_rows={total}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
