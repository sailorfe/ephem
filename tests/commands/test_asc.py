import unittest
from unittest.mock import patch, MagicMock
from ephem.commands import asc

class TestAscCommand(unittest.TestCase):

    @patch('ephem.commands.asc.print')
    @patch('ephem.commands.asc.swe.split_deg')
    @patch('ephem.commands.asc.swe.houses')
    @patch('ephem.commands.asc.swe.julday')
    @patch('ephem.commands.asc.get_locale')
    @patch('ephem.commands.asc.datetime')
    def test_run_glyphs_and_no_glyphs(self, mock_datetime, mock_get_locale, mock_julday,
                                     mock_houses, mock_split_deg, mock_print):

        mock_datetime.now.return_value = mock_datetime(2025, 8, 9, 12, 34, 56, tzinfo=None)
        mock_datetime.now.return_value = mock_datetime(2025, 8, 9, 12, 34, 56, tzinfo=mock_datetime.timezone.utc)

        mock_get_locale.return_value = (40.0, -75.0, False)
        mock_julday.return_value = 2460000.5
        mock_houses.return_value = ([0.0]*12, [180.0]*12)
        mock_split_deg.return_value = (10, 20, 30, 0, 3)

        args = MagicMock()
        args.glyphs = True

        asc.run(args)

        calls = mock_print.call_args_list
        self.assertTrue(any("AC" in str(c) and "♋︎" in str(c) for c in calls))

        mock_print.reset_mock()

        args.glyphs = False
        asc.run(args)

        calls = mock_print.call_args_list
        self.assertTrue(any("AC" in str(c) and "Can" in str(c) for c in calls))

    @patch('ephem.commands.asc.print')
    @patch('ephem.commands.asc.swe.split_deg')
    @patch('ephem.commands.asc.swe.houses')
    @patch('ephem.commands.asc.swe.julday')
    @patch('ephem.commands.asc.get_locale')
    @patch('ephem.commands.asc.datetime')
    def test_run_approx_locale_warning(self, mock_datetime, mock_get_locale, mock_julday,
                                       mock_houses, mock_split_deg, mock_print):

        mock_datetime.now.return_value = mock_datetime(2025, 8, 9, 12, 0, 0, tzinfo=mock_datetime.timezone.utc)
        mock_get_locale.return_value = (0.0, 0.0, True)
        mock_julday.return_value = 2460000.5
        mock_houses.return_value = ([0.0]*12, [180.0]*12)
        mock_split_deg.return_value = (10, 20, 30, 0, 3)

        args = MagicMock()
        args.glyphs = True

        asc.run(args)

        calls = mock_print.call_args_list
        self.assertTrue(any("No location given or found" in str(c) for c in calls))

if __name__ == '__main__':
    unittest.main()
