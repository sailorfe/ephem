from ephem.display.month import format_calendar

def run(args):
    """Main entry point for calendar command."""

    output = format_calendar(args)

    if output:  # Plain text mode
        for line in output:
            print(line)
