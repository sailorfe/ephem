import unittest
from chart.cli import parse_arguments

class test_cli(unittest.TestCase):

    def test_now_with_defaults(self):
        test_args = ["now"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "now")
        self.assertIsNotNone(args.lat)
        self.assertIsNotNone(args.lng)


    def test_now_with_coordinates(self):
        test_args = ["now", "--lat", "37.49", "--lng", "127.0855"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "now")
        self.assertEqual(args.lat, 37.49)
        self.assertEqual(args.lng, 127.0855)


    def test_cast_with_all_options(self):
        test_args = [
                "cast",
                "1998-08-26", "8:20", "Jeon Soyeon",
                "--lat", "37.49", "--lng", "127.0855",
                "--node", "mean",
                "--classical", "--brief", "--verbose",
                "--no-angles", "--no-coordinates", "--no-color"
                ]

        args = parse_arguments(test_args)

        self.assertEqual(args.command, "cast")
        self.assertEqual(args.event, ["1998-08-26", "8:20", "Jeon Soyeon"])
        self.assertEqual(args.lat, 37.49)
        self.assertEqual(args.lng, 127.0855)
        self.assertEqual(args.node, "mean")
        self.assertTrue(args.classical)
        self.assertTrue(args.brief)
        self.assertTrue(args.verbose)
        self.assertTrue(args.no_angles)
        self.assertTrue(args.no_coordinates)
        self.assertTrue(args.no_color)


    def test_cast_with_date_and_time(self):
        test_args = ["cast", "1993-08-16", "13:05", "Debian Linux"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "cast")
        self.assertEqual(args.event, ["1993-08-16", "13:05", "Debian Linux"])
        self.assertIsNone(args.lat)
        self.assertIsNone(args.lng)


    def test_cast_with_date_and_title(self):
        test_args = ["cast", "1845-05-19", "Franklin Expedition"]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "cast")
        self.assertEqual(args.event, ["1845-05-19", "Franklin Expedition"])
        self.assertIsNone(args.lat)
        self.assertIsNone(args.lng)


if __name__ == "__main__":
    unittest.main()
