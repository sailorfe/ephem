from io import StringIO
import unittest
from unittest.mock import patch, MagicMock, ANY
from argparse import Namespace
from ephem.commands import cal


class TestCal(unittest.TestCase):
    def setUp(self):
        self.args = Namespace(year=2025, month=8, offset=None, ascii=False)

    @patch("ephem.commands.cal.format_calendar")
    def test_run_basic(self, mock_format):
        """Test basic calendar generation"""
        mock_format.return_value = None

        cal.run(self.args)

        mock_format.assert_called_once_with(self.args)

    @patch("ephem.commands.cal.format_calendar")
    def test_run_with_offset(self, mock_format):
        """Test calendar with sidereal offset"""
        self.args.offset = 1
        mock_format.return_value = None

        cal.run(self.args)

        mock_format.assert_called_once_with(self.args)

    @patch("ephem.commands.cal.format_calendar")
    def test_run_ascii_mode(self, mock_format):
        """Test calendar in ASCII mode"""
        self.args.ascii = True
        mock_format.return_value = None

        cal.run(self.args)

        mock_format.assert_called_once_with(self.args)

    @patch('ephem.display.month.Console')  # Mock the Console class where it's used
    @patch('sys.stderr', new_callable=StringIO)
    def test_run_with_output(self, mock_stderr, MockConsole):
        """Test handling of text output using the rich Console."""
        mock_console_instance = MockConsole.return_value
        args = MagicMock(
            year=2025,
            month=1,
            offset=None,
            ascii=False
        )
        cal.run(args)
        MockConsole.assert_called_once()
        self.assertEqual(
            mock_console_instance.print.call_count, 
            2,
            "Console.print() should be called twice (for the title and the table)."
        )
        mock_console_instance.print.assert_any_call(ANY)

if __name__ == "__main__":
    unittest.main()
