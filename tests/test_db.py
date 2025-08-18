import unittest
import tempfile
import os
from datetime import datetime, timezone
from pathlib import Path
from ephem import db


class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary database file for each test."""
        # Create a temporary file that gets cleaned up automatically
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_file.close()
        self.test_db_path = self.temp_file.name
    
    def tearDown(self):
        """Clean up the temporary database file."""
        if os.path.exists(self.test_db_path):
            os.unlink(self.test_db_path)
    
    def test_get_db_path_with_cli_arg(self):
        """Test that CLI path takes precedence."""
        result = db.get_db_path("/custom/path.db")
        self.assertEqual(result, "/custom/path.db")
    
    def test_get_db_path_with_env_var(self):
        """Test that environment variable is used when no CLI path."""
        original_env = os.environ.get("EPHEM_DB")
        try:
            os.environ["EPHEM_DB"] = "/env/path.db"
            result = db.get_db_path()
            self.assertEqual(result, "/env/path.db")
        finally:
            # Restore original environment
            if original_env is None:
                os.environ.pop("EPHEM_DB", None)
            else:
                os.environ["EPHEM_DB"] = original_env
    
    def test_create_tables_creates_charts_table(self):
        """Test that create_tables actually creates the charts table."""
        db.create_tables(self.test_db_path)
        
        # Verify by adding a chart (which would fail if table doesn't exist)
        test_time = datetime.now(timezone.utc).isoformat()
        db.add_chart(
            name="Test Chart",
            timestamp_utc=test_time,
            timestamp_input="now",
            cli_path=self.test_db_path
        )
        
        # If we get here without an exception, the table exists
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 1)
    
    def test_add_and_retrieve_chart(self):
        """Test adding a chart and retrieving it."""
        db.create_tables(self.test_db_path)
        
        test_time = "2023-12-01T12:00:00+00:00"
        db.add_chart(
            name="Birthday Chart",
            timestamp_utc=test_time,
            timestamp_input="Dec 1, 2023 12:00 PM",
            latitude=40.7128,
            longitude=-74.0060,
            cli_path=self.test_db_path
        )
        
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 1)
        
        chart = charts[0]
        self.assertEqual(chart['name'], "Birthday Chart")
        self.assertEqual(chart['timestamp_utc'], test_time)
        self.assertEqual(chart['timestamp_input'], "Dec 1, 2023 12:00 PM")
        self.assertEqual(chart['latitude'], 40.7128)
        self.assertEqual(chart['longitude'], -74.0060)
        self.assertIsInstance(chart['id'], int)
    
    def test_add_chart_without_location(self):
        """Test adding a chart without latitude/longitude."""
        db.create_tables(self.test_db_path)
        
        test_time = "2023-12-01T12:00:00+00:00"
        db.add_chart(
            name="No Location Chart",
            timestamp_utc=test_time,
            timestamp_input="now",
            cli_path=self.test_db_path
        )
        
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 1)
        
        chart = charts[0]
        self.assertEqual(chart['name'], "No Location Chart")
        self.assertIsNone(chart['latitude'])
        self.assertIsNone(chart['longitude'])
    
    def test_get_chart_by_id(self):
        """Test retrieving a specific chart by ID."""
        db.create_tables(self.test_db_path)
        
        # Add two charts
        test_time1 = "2023-12-01T12:00:00+00:00"
        test_time2 = "2023-12-02T15:30:00+00:00"
        
        db.add_chart("Chart 1", test_time1, "input1", cli_path=self.test_db_path)
        db.add_chart("Chart 2", test_time2, "input2", cli_path=self.test_db_path)
        
        # Get the second chart by ID
        chart = db.get_chart(2, self.test_db_path)
        self.assertIsNotNone(chart)
        self.assertEqual(chart['id'], 2)
        self.assertEqual(chart['name'], "Chart 2")
        self.assertEqual(chart['timestamp_utc'], test_time2)
    
    def test_get_chart_nonexistent_id(self):
        """Test that getting a non-existent chart returns None."""
        db.create_tables(self.test_db_path)
        
        chart = db.get_chart(999, self.test_db_path)
        self.assertIsNone(chart)
    
    def test_delete_chart(self):
        """Test deleting a chart."""
        db.create_tables(self.test_db_path)
        
        # Add three charts
        test_time = "2023-12-01T12:00:00+00:00"
        for i in range(3):
            db.add_chart(f"Chart {i+1}", test_time, "input", cli_path=self.test_db_path)
        
        # Verify we have 3 charts
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 3)
        
        # Delete the middle one
        db.delete_chart(2, self.test_db_path)
        
        # Verify we now have 2 charts and the right one is gone
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 2)
        
        chart_names = [chart['name'] for chart in charts]
        self.assertIn("Chart 1", chart_names)
        self.assertIn("Chart 3", chart_names)
        self.assertNotIn("Chart 2", chart_names)
    
    def test_delete_nonexistent_chart(self):
        """Test that deleting a non-existent chart doesn't crash."""
        db.create_tables(self.test_db_path)
        
        # This should not raise an exception
        db.delete_chart(999, self.test_db_path)
        
        # And we should have no charts
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 0)
    
    def test_view_charts_empty_database(self):
        """Test viewing charts when database is empty."""
        db.create_tables(self.test_db_path)
        
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 0)
        self.assertIsInstance(charts, list)
    
    def test_multiple_charts_ordered_by_id(self):
        """Test that view_charts returns charts ordered by ID."""
        db.create_tables(self.test_db_path)
        
        # Add charts in a specific order
        test_times = [
            "2023-12-01T12:00:00+00:00",
            "2023-12-02T12:00:00+00:00", 
            "2023-12-03T12:00:00+00:00"
        ]
        
        for i, time in enumerate(test_times):
            db.add_chart(f"Chart {i+1}", time, f"input{i+1}", cli_path=self.test_db_path)
        
        charts = db.view_charts(self.test_db_path)
        self.assertEqual(len(charts), 3)
        
        # Verify they're ordered by ID
        for i, chart in enumerate(charts):
            self.assertEqual(chart['id'], i + 1)
            self.assertEqual(chart['name'], f"Chart {i + 1}")


if __name__ == '__main__':
    unittest.main()
