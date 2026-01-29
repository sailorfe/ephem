import argparse
import sqlite3
import pydoc
from . import cast
from datetime import datetime
from ephem.db import view_charts, get_chart, delete_chart


def run_loaded_chart(args):
    try:
        chart = get_chart(args.id)
    except sqlite3.OperationalError as e:
        if "no such table: charts" in str(e):
            print(
                "✨ No charts saved yet! Run `ephem cast --save` to add your first chart."
            )
            return
        raise e

    if not chart:
        print(f"No chart found with ID {args.id}")
        return

    dt = datetime.fromisoformat(chart["timestamp_utc"])
    date_str = dt.date().isoformat()
    time_str = dt.time().strftime("%H:%M:%S")

    loaded_args = argparse.Namespace(
        lat=chart["latitude"],
        lng=chart["longitude"],
        offset=None,
        event=[date_str, time_str, chart["name"]],
        timezone=None,
        save=False,
        command="cast",
        save_config=False,
        show_config=False,
    )

    display_options = [
        "no_color",
        "no_geo",
        "no_angles",
        "classical",
        "theme",
        "ascii",
        "node",
    ]
    for opt in display_options:
        setattr(loaded_args, opt, getattr(args, opt, None))

    if hasattr(args, "offset") and args.offset is not None:
        loaded_args.offset = int(args.offset)

    cast.run(loaded_args)


def print_charts(args=None):
    try:
        charts = view_charts()
    except sqlite3.OperationalError as e:
        if "no such table: charts" in str(e):
            pydoc.pager(
                "✨ No charts saved yet! Run `ephem cast --save` to add your first chart."
            )
            return
        raise e

    if not charts:
        pydoc.pager(
            "✨ No charts saved yet! Run `ephem cast --save` to add your first chart."
        )
        return

    lines = []
    for chart in charts:
        lines.append(f"[{chart['id']}] {chart['name']}")
        lines.append(f"   UTC:     {chart['timestamp_utc']}")
        lines.append(f"   Local:   {chart['timestamp_input']}")
        lines.append(f"   Lat:     {chart['latitude']}, Lng: {chart['longitude']}")
        lines.append("")  # blank line

    output = "\n".join(lines)
    pydoc.pager(output)


def delete_chart_cmd(args):
    success = delete_chart(args.id)
    if success:
        print(f"✅ Deleted chart {args.id}")
    else:
        print(f"⚠️  Chart ID {args.id} not found. Nothing deleted.")


def yaml_sync_cmd(args=None):
    try:
        from ephem.yaml_sync import full_sync

        full_sync()
    except ImportError:
        print(
            "⚠️  YAML sync functionality not available. Install PyYAML: pip install pyyaml"
        )
    except Exception as e:
        print(f"❌ Sync failed: {e}")
