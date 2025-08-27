import argparse
import sqlite3
from . import cast
from datetime import datetime
from ephem.db import view_charts, get_chart, delete_chart

def run_loaded_chart(args):
    """Run `ephem data load` as if it's `ephem cast`."""
    try:
        chart = get_chart(args.id)
    except sqlite3.OperationalError as e:
        if "no such table: charts" in str(e):
            print("✨ No charts saved yet! Run `ephem cast --save` to add your first chart.")
            return
        raise e  # Re-raise if it's a different database error

    if not chart:
        print(f"No chart found with ID {args.id}")
        return

    # parse ISO 8601 timestamp into separate date and time strings
    dt = datetime.fromisoformat(chart['timestamp_utc'])
    date_str = dt.date().isoformat()       # "YYYY-MM-DD"
    time_str = dt.time().strftime("%H:%M") # "HH:MM"

    # Create base args from chart data
    loaded_args = argparse.Namespace(
        lat=chart['latitude'],
        lng=chart['longitude'],
        offset=None,
        event=[date_str, time_str, chart['name']],
        timezone=None,
        save=False,
        command="cast"
    )

    # Copy display options from command line args
    copy_options = [
        'bare', 'anonymize', 'no_angles', 
        'classical', 'theme', 'format', 'node'
    ]
    for opt in copy_options:
        setattr(loaded_args, opt, getattr(args, opt, None))

    # Handle offset separately since it needs type conversion
    if hasattr(args, 'offset') and args.offset is not None:
        loaded_args.offset = int(args.offset)

    cast.run(loaded_args)


def print_charts(args=None, cli_path=None):
    """View chart database."""
    try:
        charts = view_charts(cli_path)
    except sqlite3.OperationalError as e:
        if "no such table: charts" in str(e):
            print("✨ No charts saved yet! Run `ephem cast --save` to add your first chart.")
            return
        raise e  # Re-raise if it's a different database error

    if not charts:
        print("✨ No charts saved yet! Run `ephem cast --save` to add your first chart.")
        return

    for chart in charts:
        print(f"[{chart['id']}] {chart['name']}")
        print(f"   UTC:   {chart['timestamp_utc']}")
        print(f"   Local: {chart['timestamp_input']}")
        print(f"   Lat: {chart['latitude']}, Lng: {chart['longitude']}")
        print()


def cli_delete_chart(args):
    """Delete chart by id."""
    delete_chart(args.id)
