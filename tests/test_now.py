import unittest
from chart.cli import parse_arguments
from chart.commands import now

class TestNowCommand(unittest.TestCase):
    def test_now_defaults(self):
        test_args = ["now"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "now")
        self.assertIsNone(args.lat)
        self.assertIsNone(args.lng)

    def test_run_with_args(self):
        test_args = ["now", "--lat", "37.49", "--lng", "127.0855"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "now")
        self.assertEqual(args.lat, 37.49)
        self.assertEqual(args.lng, 127.0855)

        try:
            now.run(args)
        except Exception as e:
            self.fail(f"now.run raised an exception: {e}")

    def test_cli_parsing(self):
        test_args = [
            "now",
            "--lat", "37.49", "--lng", "127.0855",
            "--node", "mean",
            "--classical", "--brief", "--verbose",
            "--no-angles", "--no-coordinates", "--no-color"
        ]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "now")
        self.assertEqual(args.lat, 37.49)
        self.assertEqual(args.lng, 127.0855)
        self.assertTrue(args.classical)
        self.assertTrue(args.brief)
        self.assertTrue(args.verbose)
        self.assertTrue(args.no_angles)
        self.assertTrue(args.no_coordinates)
        self.assertTrue(args.no_color)


if __name__ == "__main__":
    unittest.main()
