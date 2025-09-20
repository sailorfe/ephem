import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from ephem.config import run_save


class TestRunSaveSmoke(unittest.TestCase):
    def test_run_save_no_values(self):
        """Smoke test: run_save should handle empty/no-saveable args."""
        args = SimpleNamespace()  # no attributes set
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            run_save(args)
        output = buf.getvalue()
        self.assertIn("No settings provided", output)

    def test_run_save_minimal_args(self):
        """Smoke test: run_save runs with minimal saveable args."""
        args = SimpleNamespace(lat=42.0)  # minimal location
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            try:
                run_save(args)  # we don't care about the actual file write
            except Exception as e:
                self.fail(f"run_save raised an exception: {e}")
        # Optionally, check that it printed *something* about saving
        output = buf.getvalue()
        self.assertTrue(len(output.strip()) > 0)


if __name__ == "__main__":
    unittest.main()
