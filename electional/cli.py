import argparse
from constants import FLAGS

def parse_arguments():
    parser = argparse.ArgumentParser(description="A horoscope CLI that prints the chart of the moment by default.")
    # input
    parser.add_argument('-d', '--date', type=str, help="date YYYY-MM-DD; defaults to today")
    parser.add_argument('-t', '--time', type=str, help="UTC time as HH:MM; defaults to right now")
    parser.add_argument('--lat', type=float, help="latitude; defaults geolocated public IP coordinates")
    parser.add_argument('--lng', type=float, help="longitude; defaults geolocated public IP coordinates")
    # output
    parser.add_argument('-n', '--name', help="e.g. <Your Name>, 'Now', 'Full Moon'")
    parser.add_argument('-c', '--classical', action='store_true', help="exclude Uranus through Pluto")
    parser.add_argument('--node', choices=["true", "mean"], default="true", help="choose lunar node calculation method")
    parser.add_argument('--no-angles', action='store_true', help="disable angles")
    parser.add_argument('--no-color', action='store_true', help="disable ANSI colors")
    for flag, desc in FLAGS.items():
        parser.add_argument(f"--{flag}", action='store_true', help=desc)
    return parser.parse_args()
