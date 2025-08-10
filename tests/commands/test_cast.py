import unittest
from unittest.mock import patch, MagicMock
from ephem.commands import cast

class TestCastCommand(unittest.TestCase):

    @patch('ephem.commands.cast.format_chart')
    @patch('ephem.commands.cast.jd_to_datetime')
    @patch('ephem.commands.cast.build_horoscope')
    @patch('ephem.commands.cast.get_angles')
    @patch('ephem.commands.cast.get_planets')
    @patch('ephem.commands.cast.get_julian_days')
    @patch('ephem.commands.cast.get_locale')
    def test_run_prints_output(self, mock_get_locale, mock_get_julian_days,
                               mock_get_planets, mock_get_angles,
                               mock_build_horoscope, mock_jd_to_datetime,
                               mock_format_chart):
        mock_get_locale.return_value = (10.0, 20.0, False, False)
        mock_get_julian_days.return_value = (2451051.8472222, 2451051.8465278)
        mock_get_planets.return_value = {"planet": "data"}
        mock_get_angles.return_value = {"angle": "data"}
        mock_build_horoscope.return_value = {"horoscope": "data"}
        mock_jd_to_datetime.return_value = "1998-08-16T12:00:00Z"
        mock_format_chart.return_value = ["Line 1", "Line 2"]

        args = MagicMock()
        args.event = ['1998-08-16', '8:20', 'Test Event']

        with patch('builtins.print') as mock_print:
            cast.run(args)

        mock_print.assert_any_call("Line 1")
        mock_print.assert_any_call("Line 2")
        self.assertEqual(mock_print.call_count, 2)


class TestParseEvent(unittest.TestCase):

    def test_parse_event_empty(self):
        self.assertEqual(cast.parse_event([]), (None, None, None))

    def test_parse_event_one_arg(self):
        self.assertEqual(cast.parse_event(["1998-08-26"]), ("1998-08-26", None, None))

    def test_parse_event_two_args(self):
        self.assertEqual(cast.parse_event(["1998-08-26", "8:20"]), ("1998-08-26", "8:20", None))

    def test_parse_event_three_or_more_args(self):
        self.assertEqual(
            cast.parse_event(["1998-08-26", "8:20", "Jeon", "Soyeon"]),
            ("1998-08-26", "8:20", "Jeon Soyeon")
        )


if __name__ == '__main__':
    unittest.main()
