import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate current local ascendant.")
    parser.add_argument('-y', '--lat', type=float, help="latitude; defaults to geolocated public IP coordinates.")
    parser.add_argument('-x', '--lng', type=float, help="longitude; defaults to geocloated public IP coordiantes.")
    return parser.parse_args()
