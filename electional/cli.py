import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="A horoscope CLI that prints the chart of the moment or given date, time, and coordinates.")
    # input
    parser.add_argument('-d', '--date', type=str, help="date YYYY-MM-DD; defaults to today")
    parser.add_argument('-t', '--time', type=str, help="UTC time as HH:MM; defaults to right now")
    parser.add_argument('-y', '--lat', type=float, help="latitude; defaults to geolocated public IP coordinates")
    parser.add_argument('-x', '--lng', type=float, help="longitude; defaults to geolocated public IP coordinates")
    # output
    parser.add_argument('-n', '--name', help="e.g. <Your Name>, 'Now', 'Full Moon'")
    parser.add_argument('-s', '--short', action='store_true', help="print truncated placements, e.g. 21 Sco 2")
    parser.add_argument('-p', '--plain', action='store_true', help="disable ANSI colors")
    parser.add_argument('-c', '--classical', action='store_true', help="exclude Uranus through Pluto")
    parser.add_argument('-a', '--approximate', action='store_true', help="given a date but no time and/or place, use UTC noon and don't print angles")
    parser.add_argument('--node', choices=["true", "mean"], default="true", help="choose lunar node calculation method")
    return parser.parse_args()
