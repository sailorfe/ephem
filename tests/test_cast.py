import unittest
from argparse import Namespace
from chart.cli import parse_arguments
from chart.commands import cast

class TestCastCommand(unittest.TestCase):
    def test_parse_event(self):
        event = ["1998-08-26", "08:20", "Jeon Soyeon"]
        date, time, title = cast.parse_event(event)
        self.assertEqual(date, "1998-08-26")
        self.assertEqual(time, "08:20")
        self.assertEqual(title, "Jeon Soyeon")

    def test_parse_arguments_cast(self):
        args = parse_arguments(["cast", "1998-08-26", "08:20", "Jeon Soyeon"])
        self.assertEqual(args.command, "cast")

    def test_run_with_args(self):
        test_args = Namespace(
            event=["1998-08-26", "08:20", "Jeon Soyeon"],
            lat=37.49,
            lng=127.0855,
            node="mean",
            classical=True,
            brief=True,
            verbose=True,
            no_angles=True,
            no_coordinates=True,
            no_color=True,
            save_config=False,
            command="cast"
        )

        try:
            cast.run(test_args)
        except Exception as e:
            self.fail(f"cast.run raised an exception: {e}")

    def test_cli_parsing(self):
        test_args = [
            "cast", "1998-08-26", "08:20", "Jeon Soyeon",
            "--lat", "37.49", "--lng", "127.0855",
            "--node", "mean",
            "--classical", "--brief", "--verbose",
            "--no-angles", "--no-coordinates", "--no-color"
        ]
        args = parse_arguments(test_args)
        self.assertEqual(args.command, "cast")
        self.assertEqual(args.event, ["1998-08-26", "08:20", "Jeon Soyeon"])
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
