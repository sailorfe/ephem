import unittest
from zoneinfo import ZoneInfo
from ephem.commands import cast


class TestCast(unittest.TestCase):
    def test_parse_event_empty(self):
        result = cast.parse_event([])
        self.assertEqual(result, (None, None, None))

    def test_parse_event_date_only(self):
        result = cast.parse_event(["2025-08-18"])
        self.assertEqual(result, ("2025-08-18", None, None))

    def test_parse_event_date_and_time(self):
        result = cast.parse_event(["2025-08-18", "15:30:00"])
        self.assertEqual(result, ("2025-08-18", "15:30:00", None))

    def test_parse_event_with_title(self):
        result = cast.parse_event(["2025-08-18", "15:30:00", "Test", "Chart"])
        self.assertEqual(result, ("2025-08-18", "15:30:00", "Test Chart"))

    def test_get_moment_utc(self):
        dt_local, dt_utc, approx = cast.get_moment("2025-08-18", "15:30:00")

        self.assertEqual(dt_local.year, 2025)
        self.assertEqual(dt_local.month, 8)
        self.assertEqual(dt_local.day, 18)
        self.assertEqual(dt_local.hour, 15)
        self.assertEqual(dt_local.minute, 30)
        self.assertEqual(dt_local.second, 00)
        self.assertEqual(dt_local.tzinfo, ZoneInfo("UTC"))

        self.assertEqual(dt_utc, dt_local)  # Should be same since both UTC
        self.assertFalse(approx)


if __name__ == "__main__":
    unittest.main()
