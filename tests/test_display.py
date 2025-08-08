import unittest
from argparse import Namespace
from datetime import datetime
from chart import format_chart

class TestFormatChart(unittest.TestCase):

    def setUp(self):
        self.args = Namespace(
            command="cast",
            title="Test Chart",
            no_coordinates=False,
            verbose=False,
            brief=True,
            classical=False,
            node="mean",
            no_color=True,
            shift=False
        )

        self.lat = 0.0
        self.lng = 0.0
        self.dt = datetime(2025, 8, 7, 12, 0)

        self.planets = [
            {"lng": 335.0},
            {"lng": 323.0},
            {"lng": 178.0}
        ]

        self.horoscope = {
            "ae": {"short": "5 Pis 0"},
            "ag": {"short": "28 Vir 0"},
            "hg": {"short": "23 Aqu 0"}
        }

    def test_format_chart_returns_lines(self):
        lines = format_chart(
            self.args,
            self.lat,
            self.lng,
            self.dt,
            self.horoscope,
            self.planets,
            approx_time=True,
            approx_locale=True
        )

        self.assertIsInstance(lines, list)
        self.assertTrue(any("Test Chart" in line for line in lines))
        self.assertTrue(any("Pis" in line for line in lines))
        self.assertTrue(any("Vir" in line for line in lines))
        self.assertTrue(any("Aqu" in line for line in lines))

    def test_no_coordinates_flag(self):
        self.args.no_coordinates = True
        lines = format_chart(
            self.args,
            self.lat,
            self.lng,
            self.dt,
            self.horoscope,
            self.planets,
            approx_time=False,
            approx_locale=False
        )
        self.assertFalse(any("@" in line for line in lines))  # No geo string

if __name__ == "__main__":
    unittest.main()
