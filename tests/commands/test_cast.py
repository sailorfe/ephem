import unittest
from unittest.mock import patch, MagicMock
from ephem.commands import cast

class TestCastCommand(unittest.TestCase):

    def test_parse_event(self):
        # Test different lengths of event args
        self.assertEqual(cast.parse_event([]), (None, None, None))
        self.assertEqual(cast.parse_event(['2025-08-09']), ('2025-08-09', None, None))
        self.assertEqual(cast.parse_event(['2025-08-09', '12:00']), ('2025-08-09', '12:00', None))
        self.assertEqual(cast.parse_event(['2025-08-09', '12:00', 'My', 'Event']), 
                         ('2025-08-09', '12:00', 'My Event'))

    def test_get_moment(self):
        # Explicit date and time -> approx_time False
        self.assertEqual(cast.get_moment('2025-08-09', '12:00'), ('2025-08-09', '12:00', False))
        # Date but no time -> approximate noon, approx_time True
        self.assertEqual(cast.get_moment('2025-08-09', None), ('2025-08-09', '12:00', True))
        # Neither date nor time -> all None except approx_time True
        self.assertEqual(cast.get_moment(None, None), (None, None, True))

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
        mock_get_julian_days.return_value = (2459488.0, 2459487.5)
        mock_get_planets.return_value = {"planet": "data"}
        mock_get_angles.return_value = {"angle": "data"}
        mock_build_horoscope.return_value = {"horoscope": "data"}
        mock_jd_to_datetime.return_value = "2025-08-09T12:00:00Z"
        mock_format_chart.return_value = ["Line 1", "Line 2"]

        args = MagicMock()
        args.event = ['2025-08-09', '12:00', 'Test Event']

        with patch('builtins.print') as mock_print:
            cast.run(args)

        mock_print.assert_any_call("Line 1")
        mock_print.assert_any_call("Line 2")
        self.assertEqual(mock_print.call_count, 2)

if __name__ == '__main__':
    unittest.main()
