import unittest
from unittest.mock import patch
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

    @patch("ephem.commands.cal.format_calendar")
    def test_run_with_output(self, mock_format):
        """Test handling of text output if returned"""
        mock_format.return_value = ["Line 1", "Line 2"]

        with patch("builtins.print") as mock_print:
            cal.run(self.args)

            mock_print.assert_any_call("Line 1")
            mock_print.assert_any_call("Line 2")
            self.assertEqual(mock_print.call_count, 2)


if __name__ == "__main__":
    unittest.main()
