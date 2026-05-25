import fs from "node:fs";
import { neon } from "@neondatabase/serverless";

const FALLBACK_IMAGES = [
  "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=85",
];

function readEnv(path) {
  if (!fs.existsSync(path)) return {};
  const env = {};
  for (const line of fs.readFileSync(path, "utf8").split(/\n/)) {
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const [key, ...rest] = line.split("=");
    env[key.trim()] = rest.join("=").trim();
  }
  return env;
}

function firstLine(text) {
  const lines = (text || "")
    .split(/\n/)
    .map((line) => line.replace(/[🏠📍💲📆❗️]/g, "").trim())
    .filter(Boolean);
  return lines.find((line) => /квартира/i.test(line)) || lines.find((line) => !/в\s*и\s*д\s*е\s*о|видео/i.test(line));
}

function detectFloor(text) {
  const match = (text || "").match(/\((\d+\s*\/\s*\d+)\s*этаж\)/i);
  return match ? match[1].replace(/\s+/g, "") : "—";
}

function featureList(row) {
  const features = [];
  if (row.has_video) features.push("Видео");
  if (row.allows_kids) features.push("Можно с детьми");
  if (row.has_pets) features.push("Можно с животными");
  if (row.is_new_build) features.push("Новострой");
  return features;
}

const env = { ...readEnv(".env.neon"), ...process.env };
const databaseUrl = env.NEON_DATABASE_URL || env.DATABASE_URL;
if (!databaseUrl) {
  console.error("No NEON_DATABASE_URL or DATABASE_URL found. Check .env.neon.");
  process.exit(1);
}

const sql = neon(databaseUrl);
const rows = await sql`
  select
    id,
    first_message_id,
    posted_at,
    raw_text,
    district,
    rooms,
    price_eur,
    status,
    address,
    has_pets,
    allows_kids,
    is_new_build,
    has_video,
    media_count
  from telegram_listings
  order by posted_at desc, id desc
  limit 100
`;

const listings = rows.map((row, index) => ({
  id: Number(row.first_message_id || row.id),
  title: firstLine(row.raw_text) || `${row.rooms || ""}-комнатная квартира`.trim(),
  district: row.district || "Кишинев",
  address: row.address || "Адрес из Telegram",
  price: Number(row.price_eur || 0),
  rooms: Number(row.rooms || 0),
  floor: detectFloor(row.raw_text),
  status: row.status || "active",
  date: new Date(row.posted_at).toISOString().slice(0, 10),
  image: FALLBACK_IMAGES[index % FALLBACK_IMAGES.length],
  video: Boolean(row.has_video),
  kids: Boolean(row.allows_kids),
  pets: Boolean(row.has_pets),
  newBuild: Boolean(row.is_new_build),
  source: "https://t.me/",
  description: row.raw_text || "",
  features: featureList(row),
  mediaCount: Number(row.media_count || 0),
}));

fs.writeFileSync("web/listings.json", `${JSON.stringify(listings, null, 2)}\n`);
console.log(`Exported ${listings.length} listings to web/listings.json`);
