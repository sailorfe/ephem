import unittest
from unittest.mock import patch, mock_open
from chart import now
from datetime import datetime

class TestNow(unittest.TestCase):
    def test_get_moment_now(self):
        args = type('Args', (object,), {"command": "now", "date": None, "time": None})()
        date_str, time_str, approx = now.get_moment(args)
        self.assertIsInstance(date_str, str)
        self.assertIsInstance(time_str, str)
        self.assertFalse(approx)

    def test_get_moment_cast_datetime(self):
        args = type('Args', (object,), {"command": "cast", "date": "1993-08-16", "time": "13:05"})
        date_str, time_str, approx = now.get_moment(args)
        self.assertEqual(date_str, "1993-08-16")
        self.assertEqual(time_str, "13:05")
        self.assertFalse(approx)

    def test_get_moment_cast_date(self):
        args = type('Args', (object,), {"command": "cast", "date": "1845-05-19", "time": None})
        date_str, time_str, approx = now.get_moment(args)
        self.assertEqual(date_str, "1845-05-19")
        self.assertEqual(time_str, "12:00")
        self.assertTrue(approx)

    @patch("os.path.expanduser", return_value="/fake/path/chart.ini")
    @patch("builtins.open", new_callable=mock_open, read_data="[location]\nlat = 42.0\nlng = -71.0")
    def test_get_locale_from_config(self, mock_open, mock_expanduser):
        args = type('Args', (object,), {"lat": None, "lng": None})()
        lat, lng, approx = now.get_locale(args)
        self.assertEqual(lat, 42.0)
        self.assertEqual(lng, -71.0)
        self.assertTrue(approx)

    def test_get_locale_from_args(self):
        args = type('Args', (object,), {"lat": 10.0, "lng": 20.0})()
        lat, lng, approx = now.get_locale(args)
        self.assertEqual((lat, lng), (10.0, 20.0))
        self.assertFalse(approx)

if __name__ == '__main__':
    unittest.main()
