import unittest
from chart.cli import parse_arguments
from chart.commands import asc

class TestAscCommand(unittest.TestCase):
    def test_asc(self):
        test_args = ["asc"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "asc")
        self.assertIsNone(args.lat)
        self.assertIsNone(args.lng)

    def test_run_with_args(self):
        test_args = ["asc", "--lat", "37.49", "--lng", "127.0855"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "asc")
        self.assertEqual(args.lat, 37.49)
        self.assertEqual(args.lng, 127.0855)

        try:
            asc.run(args)
        except Exception as e:
            self.fail(f"asc.run raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
