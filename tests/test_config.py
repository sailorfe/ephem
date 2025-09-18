import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from ephem.config import (
    run_save, validate_config_values, should_save_value,
    load_config_defaults, parse_float_field, validate_offset_field
)

class TestConfig(unittest.TestCase):
    def test_parse_float_field(self):
        """Test float field parsing."""
        self.assertEqual(parse_float_field("42.5"), 42.5)
        self.assertEqual(parse_float_field("-12.3"), -12.3)
        self.assertIsNone(parse_float_field("invalid"))
        self.assertIsNone(parse_float_field(None))

    def test_validate_offset_field(self):
        """Test zodiac offset validation."""
        self.assertEqual(validate_offset_field(0), 0)
        self.assertEqual(validate_offset_field(46), 46)
        self.assertIsNone(validate_offset_field(47))
        self.assertIsNone(validate_offset_field(-1))
        self.assertIsNone(validate_offset_field(None))
        self.assertIsNone(validate_offset_field("invalid"))

    def test_validate_config_values(self):
        """Test coordinate validation."""
        # Valid cases
        validate_config_values(0, 0)  # Should not raise
        validate_config_values(90, 180)  # Should not raise
        validate_config_values(-90, -180)  # Should not raise
        
        # Invalid cases
        with self.assertRaises(ValueError):
            validate_config_values(91, 0)
        with self.assertRaises(ValueError):
            validate_config_values(-91, 0)
        with self.assertRaises(ValueError):
            validate_config_values(0, 181)
        with self.assertRaises(ValueError):
            validate_config_values(0, -181)

    def test_should_save_value(self):
        """Test save value determination logic."""
        # Boolean flags
        self.assertTrue(should_save_value("no_geo", True))
        self.assertFalse(should_save_value("no_geo", False))
        self.assertFalse(should_save_value("no_geo", None))

        # Choice options
        self.assertFalse(should_save_value("node", "true"))  # default
        self.assertTrue(should_save_value("node", "mean"))
        self.assertFalse(should_save_value("theme", "sect"))  # default
        self.assertTrue(should_save_value("theme", "mode"))

        # Location and zodiac
        self.assertTrue(should_save_value("lat", 42.0))
        self.assertTrue(should_save_value("lng", -73.0))
        self.assertTrue(should_save_value("offset", 23))
        self.assertFalse(should_save_value("lat", None))

    @patch("ephem.config.tomli_w")
    @patch("ephem.config.get_config_path")
    def test_run_save(self, mock_get_path, mock_tomli_w):
        """Test config save functionality."""
        mock_path = MagicMock()
        mock_get_path.return_value = mock_path
        mock_tomli_w.dump = MagicMock()

        # Test saving valid coordinates
        args = SimpleNamespace(lat=45.0, lng=-73.0)
        with patch("builtins.open", mock_open()) as mock_file:
            run_save(args)
            mock_file.assert_called()
            mock_tomli_w.dump.assert_called_once()

        # Test with no saveable values
        args = SimpleNamespace(no_geo=False)
        with patch("builtins.open", mock_open()) as mock_file:
            run_save(args)
            mock_file.assert_not_called()

    @patch("ephem.config.get_config_path")
    def test_load_config_defaults(self, mock_get_path):
        """Test loading config defaults."""
        mock_path = MagicMock()
        mock_get_path.return_value = mock_path

        # Test with non-existent file
        mock_path.exists.return_value = False
        self.assertEqual(load_config_defaults(), {})

        # Test with valid config
        mock_path.exists.return_value = True
        test_config = {
            "location": {"lat": 42.0, "lng": -73.0},
            "display": {"no-geo": True, "theme": "mode"}
        }
        
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("tomllib.load", return_value=test_config):
                defaults = load_config_defaults()
                self.assertEqual(defaults["lat"], 42.0)
                self.assertEqual(defaults["lng"], -73.0)
                self.assertEqual(defaults["no_geo"], True)
                self.assertEqual(defaults["theme"], "mode")

if __name__ == "__main__":
    unittest.main()
