import unittest
import os
import shutil
from pathlib import Path
from argparse import Namespace
from ephem.commands import config

class TestConfig(unittest.TestCase):
    def setUp(self):
        """Create a temporary config path for testing."""
        self.test_dir = Path("/tmp/ephem_test_config")
        self.test_config_dir = self.test_dir / "ephem"
        self.test_file = self.test_config_dir / "ephem.ini"
        os.environ["XDG_CONFIG_HOME"] = str(self.test_dir)

    def tearDown(self):
        """Clean up test config directory and files."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_get_config_path(self):
        """Test config path resolution."""
        path = config.get_config_path()
        self.assertEqual(path, self.test_file)

    def test_load_config_empty(self):
        """Test loading when no config exists."""
        # Ensure no config exists
        if self.test_file.exists():
            self.test_file.unlink()
        defaults = config.load_config_defaults()
        self.assertEqual(defaults, {})

    def test_save_and_load_location(self):
        """Test saving and loading location settings."""
        # Save test location
        args = Namespace(lat=51.5074, lng=-0.1278)
        config.run_save(args)

        # Verify file was created
        self.assertTrue(self.test_file.exists())

        # Load and verify settings
        defaults = config.load_config_defaults()
        self.assertEqual(defaults.get('lat'), 51.5074)
        self.assertEqual(defaults.get('lng'), -0.1278)

    def test_save_partial_location(self):
        """Test saving only latitude."""
        # Ensure clean state
        if self.test_file.exists():
            self.test_file.unlink()

        args = Namespace(lat=51.5074, lng=None)
        config.run_save(args)

        defaults = config.load_config_defaults()
        self.assertEqual(defaults.get('lat'), 51.5074)
        self.assertIsNone(defaults.get('lng'))

    def test_save_no_location(self):
        """Test save with no location provided."""
        # Ensure clean state
        if self.test_file.exists():
            self.test_file.unlink()

        args = Namespace(lat=None, lng=None)
        config.run_save(args)

        self.assertFalse(self.test_file.exists())

if __name__ == '__main__':
    unittest.main()
