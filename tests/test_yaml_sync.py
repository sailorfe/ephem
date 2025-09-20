import unittest
from unittest.mock import patch
from datetime import datetime
from pathlib import Path
from ephem.yaml_sync import (
    slugify,
    get_charts_dir,
    chart_to_yaml_dict,
    yaml_dict_to_chart,
    get_yaml_filename,
    find_chart_by_content,
    sync_yaml_to_db,
    full_sync,
)


class TestYamlSync(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.sample_chart = {
            "id": 1,
            "name": "Test Chart",
            "timestamp_utc": "2025-09-10T12:00:00",
            "timestamp_input": "2025-09-10 08:00:00-04:00",
            "latitude": 40.7128,
            "longitude": -74.0060,
        }

        self.sample_yaml_dict = {
            "name": "Test Chart",
            "timestamp_utc": "2025-09-10T12:00:00",
            "timestamp_input": "2025-09-10 08:00:00-04:00",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "_metadata": {
                "created": "2025-09-10T12:00:00",
                "source": "ephem_cli",
                "tags": [],
            },
        }

    def test_slugify(self):
        """Test slug generation for filenames."""
        tests = [
            ("Test Chart", "test-chart"),
            ("Test Chart!@#$%", "test-chart"),
            ("test--chart  name", "test-chart-name"),
            ("", ""),
            ("   ", ""),
            ("Hello World 123", "hello-world-123"),
        ]

        for input_text, expected in tests:
            with self.subTest(input_text=input_text):
                self.assertEqual(slugify(input_text), expected)

    @patch("ephem.yaml_sync.get_db_path")
    def test_get_charts_dir(self, mock_get_db_path):
        """Test charts directory path resolution."""
        mock_get_db_path.return_value = Path("/mock/db/ephem.db")
        expected = Path("/mock/db/charts")
        self.assertEqual(get_charts_dir(), expected)

    def test_chart_to_yaml_dict(self):
        """Test conversion from database format to YAML format."""
        with patch("ephem.yaml_sync.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.fromisoformat(
                "2025-09-10T12:00:00"
            )
            mock_datetime.fromisoformat = (
                datetime.fromisoformat
            )  # needed if chart_to_yaml_dict calls it

            result = chart_to_yaml_dict(self.sample_chart)

            self.assertEqual(result["name"], "Test Chart")
            self.assertEqual(result["timestamp_utc"], "2025-09-10T12:00:00")
            self.assertEqual(result["latitude"], 40.7128)
            self.assertEqual(result["longitude"], -74.0060)
            self.assertEqual(result["_metadata"]["source"], "ephem_cli")

    def test_yaml_dict_to_chart(self):
        """Test conversion from YAML format to database format."""
        result = yaml_dict_to_chart(self.sample_yaml_dict, "test-chart.yaml")

        self.assertEqual(result["name"], "Test Chart")
        self.assertEqual(result["timestamp_utc"], "2025-09-10T12:00:00")
        self.assertEqual(result["latitude"], 40.7128)
        self.assertEqual(result["longitude"], -74.0060)

    def test_get_yaml_filename(self):
        """Test YAML filename generation."""
        tests = [
            ("Test Chart", "test-chart.yaml"),
            ("Test Chart!@#$%", "test-chart.yaml"),
            ("", "unnamed-chart.yaml"),
            ("   ", "unnamed-chart.yaml"),
        ]

        for input_name, expected in tests:
            with self.subTest(input_name=input_name):
                self.assertEqual(get_yaml_filename(input_name), expected)

    def test_find_chart_by_content(self):
        """Test matching chart content in database."""
        db_charts = [self.sample_chart]

        # Test exact match
        result = find_chart_by_content(self.sample_chart, db_charts)
        self.assertEqual(result, self.sample_chart)

        # Test no match
        modified_chart = self.sample_chart.copy()
        modified_chart["name"] = "Different Name"
        result = find_chart_by_content(modified_chart, db_charts)
        self.assertIsNone(result)

    @patch("ephem.yaml_sync.find_yaml_files")
    @patch("ephem.yaml_sync.view_charts")
    @patch("ephem.yaml_sync.load_yaml_chart")
    @patch("ephem.yaml_sync.add_chart")
    def test_sync_yaml_to_db(
        self, mock_add_chart, mock_load_yaml, mock_view_charts, mock_find_files
    ):
        """Test YAML to database synchronization."""
        mock_find_files.return_value = [Path("test-chart.yaml")]
        mock_view_charts.return_value = []
        mock_load_yaml.return_value = self.sample_chart

        results = sync_yaml_to_db()

        self.assertEqual(len(results["added"]), 1)
        self.assertEqual(len(results["errors"]), 0)
        mock_add_chart.assert_called_once()

    @patch("ephem.yaml_sync.create_tables")
    @patch("ephem.yaml_sync.find_yaml_files")
    @patch("ephem.yaml_sync.view_charts")
    @patch("ephem.yaml_sync.export_chart_to_yaml")
    @patch("ephem.yaml_sync.sync_yaml_to_db")
    def test_full_sync(
        self,
        mock_sync_db,
        mock_export,
        mock_view_charts,
        mock_find_files,
        mock_create_tables,
    ):
        """Test full bidirectional synchronization."""
        mock_find_files.return_value = []
        mock_view_charts.return_value = [self.sample_chart]
        mock_sync_db.return_value = {"added": [], "errors": [], "conflicts": []}

        full_sync()

        mock_create_tables.assert_called_once()
        mock_export.assert_called_once()
        mock_sync_db.assert_called_once()


if __name__ == "__main__":
    unittest.main()
