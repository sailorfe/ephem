import unittest
from argparse import Namespace
from ephem.commands import asc
from ephem.constants import SIGNS

class TestAsc(unittest.TestCase):
    def test_sign_from_index(self):
        """Test sign lookup from index."""
        # Test first sign (Aries)
        name, data = asc.sign_from_index(0)
        self.assertEqual(name, "Aries")
        self.assertEqual(data["glyph"], "♈︎")
        self.assertEqual(data["trunc"], "Ari")

        # Test middle sign (Libra)
        name, data = asc.sign_from_index(6)
        self.assertEqual(name, "Libra")
        self.assertEqual(data["glyph"], "♎︎")
        self.assertEqual(data["trunc"], "Lib")

        # Test last sign (Pisces)
        name, data = asc.sign_from_index(11)
        self.assertEqual(name, "Pisces")
        self.assertEqual(data["glyph"], "♓︎")
        self.assertEqual(data["trunc"], "Pis")


def test_run_basic(self):
    """Test basic ascendant calculation."""
    args = Namespace(
        lat=0,
        lng=0,
        offset=None,
        glyphs=False
    )
    output = asc.run(args)
    # Check output contains AC and degrees/sign/minutes
    self.assertIsNotNone(output, "Output should not be None")
    self.assertIn("AC", output)
    # Check format matches "AC DD Sign MM" (e.g. "AC 14 Aqu 36")
    self.assertRegex(output, r"AC \d{1,2} [A-Z][a-z]{2} \d{1,2}")


if __name__ == '__main__':
    unittest.main()
