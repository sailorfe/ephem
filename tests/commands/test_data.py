import unittest
from unittest.mock import patch, MagicMock
import argparse
import sqlite3
from datetime import datetime
from ephem.commands import data

class TestDataCommands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.sample_chart = {
            'id': 1,
            'name': 'Test Chart',
            'timestamp_utc': '2025-09-10T12:00:00',
            'timestamp_input': '2025-09-10 08:00:00-04:00',
            'latitude': 40.7128,
            'longitude': -74.0060
        }
        
        self.test_args = argparse.Namespace(
            id=1,
            offset=None,
            no_color=False,
            no_geo=False,
            no_angles=False,
            classical=False,
            theme=None,
            ascii=False,
            node=None
        )

    @patch('ephem.commands.data.get_chart')
    @patch('ephem.commands.data.cast.run')
    def test_run_loaded_chart_success(self, mock_cast_run, mock_get_chart):
        """Test successful chart loading and execution."""
        mock_get_chart.return_value = self.sample_chart
        
        data.run_loaded_chart(self.test_args)
        
        mock_get_chart.assert_called_once_with(1)
        mock_cast_run.assert_called_once()
        
        # Verify the args passed to cast.run
        called_args = mock_cast_run.call_args[0][0]
        self.assertEqual(called_args.lat, 40.7128)
        self.assertEqual(called_args.lng, -74.0060)
        self.assertEqual(called_args.command, "cast")
        self.assertEqual(called_args.event[0], "2025-09-10")
        self.assertEqual(called_args.event[1], "12:00")

    @patch('ephem.commands.data.get_chart')
    def test_run_loaded_chart_not_found(self, mock_get_chart):
        """Test handling of non-existent chart."""
        mock_get_chart.return_value = None
        
        with patch('builtins.print') as mock_print:
            data.run_loaded_chart(self.test_args)
            mock_print.assert_called_once_with("No chart found with ID 1")

    @patch('ephem.commands.data.get_chart')
    def test_run_loaded_chart_no_table(self, mock_get_chart):
        """Test handling of missing database table."""
        mock_get_chart.side_effect = sqlite3.OperationalError("no such table: charts")
        
        with patch('builtins.print') as mock_print:
            data.run_loaded_chart(self.test_args)
            mock_print.assert_called_once_with(
                "✨ No charts saved yet! Run `ephem cast --save` to add your first chart."
            )

    @patch('ephem.commands.data.view_charts')
    def test_print_charts_success(self, mock_view_charts):
        """Test successful chart listing."""
        mock_view_charts.return_value = [self.sample_chart]
        
        with patch('builtins.print') as mock_print:
            data.print_charts()
            mock_print.assert_any_call("[1] Test Chart")

    @patch('ephem.commands.data.view_charts')
    def test_print_charts_empty(self, mock_view_charts):
        """Test empty chart database."""
        mock_view_charts.return_value = []
        
        with patch('builtins.print') as mock_print:
            data.print_charts()
            mock_print.assert_called_once_with(
                "✨ No charts saved yet! Run `ephem cast --save` to add your first chart."
            )

    @patch('ephem.commands.data.delete_chart')
    def test_delete_chart_success(self, mock_delete):
        """Test successful chart deletion."""
        mock_delete.return_value = True
        args = argparse.Namespace(id=1)
        
        with patch('builtins.print') as mock_print:
            data.delete_chart_cmd(args)
            mock_print.assert_called_once_with("✅ Deleted chart 1")

    @patch('ephem.commands.data.delete_chart')
    def test_delete_chart_not_found(self, mock_delete):
        """Test deletion of non-existent chart."""
        mock_delete.return_value = False
        args = argparse.Namespace(id=999)
        
        with patch('builtins.print') as mock_print:
            data.delete_chart_cmd(args)
            mock_print.assert_called_once_with("⚠️  Chart ID 999 not found. Nothing deleted.")

    def test_yaml_sync_missing_dependency(self):
        """Test YAML sync with missing PyYAML."""
        with patch('builtins.print') as mock_print:
            with patch.dict('sys.modules', {'ephem.yaml_sync': None}):
                data.yaml_sync_cmd()
                mock_print.assert_called_once_with(
                    "⚠️  YAML sync functionality not available. Install PyYAML: pip install pyyaml"
                )

if __name__ == '__main__':
    unittest.main()