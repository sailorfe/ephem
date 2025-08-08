import unittest
from unittest.mock import patch
from chart import parse_arguments

class TestCLIArguments(unittest.TestCase):

    def test_cast_with_all_options(self):
        test_args = [
                "chart", "cast",
                "--date", "1998-08-26", "--time", "8:20",
                "--lat", "37.49", "--lng", "127.0855",
                "--title", "Jeon Soyeon",
                "--node", "mean",
                "--classical", "--brief", "--verbose",
                "--no-coordinates", "--no-color"
                ]
        with patch("sys.argv", test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "cast")
            self.assertEqual(args.date, "1998-08-26")
            self.assertEqual(args.time, "8:20")
            self.assertEqual(args.lat, 37.49)
            self.assertEqual(args.lng, 127.0855)
            self.assertEqual(args.title, "Jeon Soyeon")
            self.assertEqual(args.node, "mean")
            self.assertTrue(args.classical)
            self.assertTrue(args.brief)
            self.assertTrue(args.verbose)
            self.assertTrue(args.no_coordinates)
            self.assertTrue(args.no_color)

    def test_now_with_defaults(self):
        test_args = ["chart", "now"]
        with patch("sys.argv", test_args):
            args = parse_arguments()
            self.assertEqual(args.command, "now")
            self.assertFalse(args.no_color)

if __name__ == "__main__":
    unittest.main()
