import unittest
from unittest.mock import patch, MagicMock
from ephem.commands import now

class TestNowCommand(unittest.TestCase):

    @patch('ephem.commands.now.format_chart')
    @patch('ephem.commands.now.jd_to_datetime')
    @patch('ephem.commands.now.build_horoscope')
    @patch('ephem.commands.now.get_angles')
    @patch('ephem.commands.now.get_planets')
    @patch('ephem.commands.now.get_julian_days')
    @patch('ephem.commands.now.get_locale')
    @patch('ephem.commands.now.get_moment')
    def test_now_prints_output(self, mock_get_moment, mock_get_locale, mock_get_julian_days, 
                               mock_get_planets, mock_get_angles, mock_build_horoscope,
                               mock_jd_to_datetime, mock_format_chart):
        mock_get_moment.return_value = ("2025-08-09", "12:00", False)
        mock_get_locale.return_value = (10.0, 20.0, False, False)
        mock_get_julian_days.return_value = (2459488.0, 2459487.5)
        mock_get_planets.return_value = {"planet": "data"}
        mock_get_angles.return_value = {"angle": "data"}
        mock_build_horoscope.return_value = {"horoscope": "data"}
        mock_jd_to_datetime.return_value = "2025-08-09T12:00:00Z"
        mock_format_chart.return_value = ["Line 1", "Line 2"]

        with patch('builtins.print') as mock_print:
            now.run(args=MagicMock())

        mock_print.assert_any_call("Line 1")
        mock_print.assert_any_call("Line 2")
        self.assertEqual(mock_print.call_count, 2)

if __name__ == '__main__':
    unittest.main()
