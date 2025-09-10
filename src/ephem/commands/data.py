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
        raise e

    if not chart:
        print(f"No chart found with ID {args.id}")
        return

    # Parse ISO 8601 timestamp into separate date and time strings
    dt = datetime.fromisoformat(chart['timestamp_utc'])
    date_str = dt.date().isoformat()
    time_str = dt.time().strftime("%H:%M")

    # Create args from chart data
    loaded_args = argparse.Namespace(
        lat=chart['latitude'],
        lng=chart['longitude'],
        offset=None,
        event=[date_str, time_str, chart['name']],
        timezone=None,
        save=False,
        command="cast",
        save_config=False,
        show_config=False
    )

    # Copy display options from command line args
    display_options = [
        'no_color', 'no_geo', 'no_angles',
        'classical', 'theme', 'ascii', 'node'
    ]
    for opt in display_options:
        setattr(loaded_args, opt, getattr(args, opt, None))

    # Handle offset separately since it needs type conversion
    if hasattr(args, 'offset') and args.offset is not None:
        loaded_args.offset = int(args.offset)

    cast.run(loaded_args)


def print_charts(args=None):
    """View chart database."""
    try:
        charts = view_charts()
    except sqlite3.OperationalError as e:
        if "no such table: charts" in str(e):
            print("✨ No charts saved yet! Run `ephem cast --save` to add your first chart.")
            return
        raise e

    if not charts:
        print("✨ No charts saved yet! Run `ephem cast --save` to add your first chart.")
        return

    for chart in charts:
        print(f"[{chart['id']}] {chart['name']}")
        print(f"   UTC:   {chart['timestamp_utc']}")
        print(f"   Local: {chart['timestamp_input']}")
        print(f"   Lat: {chart['latitude']}, Lng: {chart['longitude']}")
        print()


def delete_chart_cmd(args):
    """Delete a chart by ID."""
    success = delete_chart(args.id)
    if success:
        print(f"✅ Deleted chart {args.id}")
    else:
        print(f"⚠️  Chart ID {args.id} not found. Nothing deleted.")
