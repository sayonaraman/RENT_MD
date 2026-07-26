import unittest
from unittest.mock import patch

from scan_rentals import (
    LocationResolver,
    TARGET_CHAT,
    TARGET_TOPIC,
    format_route_note,
    parse_listing,
)


TWO_ROOM = """🏠  2-комнатная квартира
📍  Рышкановка, str. Matei Basarab, 9/1
💲  550€ от 1 месяца
"""


class DestinationTests(unittest.TestCase):
    def test_telegram_source_uses_the_same_channel_as_999(self):
        self.assertEqual(TARGET_CHAT, -1004448506771)
        self.assertIsNone(TARGET_TOPIC)


class ListingFilterTests(unittest.TestCase):
    def test_accepts_two_room_riscani_in_price_range(self):
        listing = parse_listing(TWO_ROOM)
        self.assertEqual(listing["price_eur"], 550)
        self.assertEqual(listing["rooms"], 2)
        self.assertEqual(listing["address"], "Strada Matei Basarab, 9/1")

    def test_accepts_one_room_only_with_living(self):
        text = """🏠  1-комнатная квартира+ливинг
📍  Рышкановка, str. Bogdan Voievod 2/1
💲  650€
"""
        self.assertEqual(parse_listing(text)["rooms"], 1)
        self.assertIsNone(parse_listing(text.replace("+ливинг", "")))

    def test_rejects_wrong_district_or_price(self):
        self.assertIsNone(parse_listing(TWO_ROOM.replace("Рышкановка", "Чеканы")))
        self.assertIsNone(parse_listing(TWO_ROOM.replace("550€", "400€")))
        self.assertIsNone(parse_listing(TWO_ROOM.replace("550€", "750€")))

    def test_uses_lowest_offered_euro_price(self):
        listing = parse_listing(TWO_ROOM.replace("550€", "750€ от 1 месяца, 650€ от 12"))
        self.assertEqual(listing["price_eur"], 650)


class RouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_route_matrix_produces_both_walking_distances(self):
        matrix = {
            "sources_to_targets": [[
                {"distance": 0.736},
                {"distance": 1.489},
            ]],
        }
        resolver = LocationResolver()
        with patch("scan_rentals._fetch_json", return_value=matrix):
            routes = await resolver.routes(47.064476, 28.847786)
        self.assertEqual([route["key"] for route in routes], ["malinki", "kindergarten-118"])
        self.assertEqual(routes[0]["minutes_with_stroller"], 13)
        self.assertEqual(routes[1]["minutes_with_stroller"], 26)

    def test_route_note_contains_both_destinations(self):
        note = format_route_note({
            "address": "Strada Studenților 9/20",
            "walking_routes": [
                {"name": "«Малинок»", "distance_km": 0.736, "minutes_with_stroller": 13},
                {"name": "садика №118", "distance_km": 1.489, "minutes_with_stroller": 26},
            ],
        })
        self.assertIn("До «Малинок»: 0.7 км", note)
        self.assertIn("До садика №118: 1.5 км", note)
        self.assertIn("26 мин с ребёнком и коляской", note)


if __name__ == "__main__":
    unittest.main()
