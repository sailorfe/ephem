import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
from ephem.config import run_save

class TestConfig(unittest.TestCase):
    @patch("ephem.config.tomli_w")  # mock the tomli_w module in config.py
    def test_validate_config_values(self, mock_tomli_w):
        """Test that invalid coordinates raise ValueError."""
        # Make dump a MagicMock so it does nothing
        mock_tomli_w.dump = MagicMock()

        # Invalid latitude
        args = SimpleNamespace(lat=91.0, lng=0.0)
        with self.assertRaises(ValueError):
            run_save(args)

        # Invalid longitude
        args = SimpleNamespace(lat=0.0, lng=181.0)
        with self.assertRaises(ValueError):
            run_save(args)

    @patch("ephem.config.tomli_w")
    def test_valid_coordinates(self, mock_tomli_w):
        """Test that valid coordinates do not raise an error and call tomli_w.dump."""
        mock_tomli_w.dump = MagicMock()

        args = SimpleNamespace(lat=45.0, lng=-73.0)
        try:
            run_save(args)  # should not raise
        except ValueError:
            self.fail("run_save() raised ValueError unexpectedly with valid coordinates")

        # Ensure dump was called
        mock_tomli_w.dump.assert_called_once()

if __name__ == "__main__":
    unittest.main()
