from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text
from .constants import AYANAMSAS, Colors

def get_chart_title(title=None, approx_time=False, approx_locale=False, offset=None):
    """
    Returns chart title string with optional hyp. and zodiac info inline.

    Args:
        title (str | None): User-provided chart title.
        approx_time (bool): Whether the time is approximate.
        approx_locale (bool): Whether the location is approximate.
        offset (int | str | None): Sidereal offset (None = Tropical).

    Returns:
        str: Formatted chart title line.
    """
    # Base title
    title_str = title or ""

    # Approximation marker
    if approx_time or approx_locale:
        title_str += " hyp."

    # Zodiac mode
    if offset is None:
        zodiac_info = "Tropical"
    else:
        # Convert numeric index to key
        if isinstance(offset, int) or (isinstance(offset, str) and offset.isdigit()):
            idx = int(offset)
            try:
                key = list(AYANAMSAS.keys())[idx]
            except IndexError:
                key = f"Unknown({offset})"
        else:
            key = offset

        zodiac_info = f"Sidereal — {key}"

    # Inline final title
    return f"{title_str} ({zodiac_info})"


def get_chart_subtitle(dt_local, dt_utc, lat, lng, args, approx_locale):
    """
    Returns a tuple of (time_line, location_line) for chart subtitles.

    - Shows UTC only if it differs from local time.
    - Optionally hides location if anonymized or approximate.
    """
    local_str = dt_local.strftime("%Y-%m-%d %H:%M %Z")  # e.g. 2025-08-09 07:54 EDT
    utc_str = dt_utc.strftime("%Y-%m-%d %H:%M UTC")

    # Show UTC only if it differs
    if local_str == utc_str:
        time_part = local_str
    else:
        time_part = f"{local_str} | {utc_str}"

    # Show location if allowed
    if not args.anonymize and not approx_locale:
        location_part = f"@ {lat} {lng}"
    else:
        location_part = ""

    return time_part, location_part


def get_warnings(args, approx_time, approx_locale, config_locale):
    """Return warnings for incomplete data to display above chart."""
    warning_conditions = [
        (approx_time, "No time provided. Using UTC noon and not printing angles."),
        (approx_locale, "No valid location provided or found in config. No angles will be printed."),
        (config_locale and args.command == "cast", "Using location from config file.")
    ]
    return [msg for cond, msg in warning_conditions if cond]


def get_mercury_sect_color(planets, default_color):
    """Check if Mercury is diurnal or nocturnal for sect color scheme (default)."""
    try:
        hg_lng = planets[2]['lng']  # hg index
        ae_lng = planets[0]['lng']  # sun index
    except (IndexError, KeyError):
        return default_color
    return "red" if hg_lng < ae_lng else "blue"


def get_spheres(horoscope, args, planets, approx_time, approx_locale):
    """Assemble list of objects to display and their element/mode colors."""
    ELEMENT_COLORS = {
        "fire": "red",
        "earth": "green",
        "air": "yellow",
        "water": "blue"
    }
    MODE_COLORS = {
        "cardinal": "magenta",
        "fixed": "bright_green",
        "mutable": "cyan"
    }
    THEME_COLORS = {
        "element": ELEMENT_COLORS,
        "mode": MODE_COLORS,
        "sect": None
    }

    if args.theme == "sect":
        spheres = [
            ("ae", "bright_red"), ("ag", "bright_blue"), ("hg", None),
            ("cu", "blue"), ("fe", "blue"), ("sn", "red"), ("pb", "red"),
            ("ura", None), ("nep", None), ("plu", None),
            ("mean_node", None), ("true_node", None),
            ("asc", None), ("mc", None)
        ]
        # hg sect
        final_spheres = []
        for key, default_color in spheres:
            if key == "hg":
                color = get_mercury_sect_color(planets, default_color)
            else:
                color = default_color
            final_spheres.append((key, color))
            spheres = final_spheres

    else:
        color_map = THEME_COLORS.get(args.theme)
        spheres = [
            (key, color_map.get(data["trip" if args.theme == "element" else "quad"]))
            for key, data in horoscope.items()
        ]

    # apply filtering flags
    if args.classical:
        spheres = [(k, c) for k, c in spheres if k not in ("ura", "nep", "plu")]
    if approx_time or approx_locale or args.no_angles:
        spheres = [(k, c) for k, c in spheres if k not in ("asc", "mc")]
    if args.node == "true":
        spheres = [(k, c) for k, c in spheres if k != "mean_node"]
    else:
        spheres = [(k, c) for k, c in spheres if k != "true_node"]

    return spheres


def render_sphere_lines(spheres, horoscope, args, colors):
    """Apply formatting objects and color schemes."""
    lines = []
    for key, color in spheres:
        data = horoscope.get(key, {})

        if args.format == "names":
            obj_name = data.get("obj_name", key).ljust(12)
            placement = data.get("full", "??")
        elif args.format == "glyphs":
            obj_name = data.get("obj_glyph", key.upper()).ljust(6)
            placement = data.get("glyph", "??")
        elif args.format == "short":
            obj_name = data.get("obj_glyph", key.upper()).ljust(6)
            placement = data.get("short", "??")
        else:
            obj_name = data.get("obj_glyph", key.upper()).ljust(6)
            placement = data.get("full", "??")

        line = f"{obj_name} {placement}"
        if colors and color:
            line = colors.colorize(line, color)
        lines.append(line)
    return lines


console = Console()

def format_chart(args, title, lat, lng, dt_local, dt_utc, horoscope, planets, approx_time, approx_locale, config_locale):
    offset = getattr(args, 'offset', None)

    """If --no-color, print bare chart; otherwise print Rich table."""
    if args.bare:
        colors = Colors(False if args.bare else True)
        lines = []

        # title + warnings
        lines.extend(get_warnings(args, approx_time, approx_locale, config_locale))
        lines.append(get_chart_title(title, approx_time, approx_locale, offset))

        # For bare mode, join subtitle parts into one line for simplicity
        time_str, location_str = get_chart_subtitle(dt_local, dt_utc, lat, lng, args, approx_locale)
        subtitle_line = time_str
        if location_str:
            subtitle_line += " " + location_str
        lines.append(subtitle_line)

        # body
        spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
        lines.extend(render_sphere_lines(spheres, horoscope, args, colors))

        return lines

    else:
        colors = Colors()
        # print warnings in yellow
        warnings = get_warnings(args, approx_time, approx_locale, config_locale)
        for warning in warnings:
            console.print(Text(warning, style="yellow"))

        # centered bold title
        chart_title = get_chart_title(title, approx_time, approx_locale, offset)
        time_str, location_str = get_chart_subtitle(dt_local, dt_utc, lat, lng, args, approx_locale)
        console.print(Align.center(Text(chart_title, style="bold")))
        console.print(Align.center(Text(time_str, style="bold")))
        if location_str:
            console.print(Align.center(Text(location_str, style="bold")))
        console.print()  # Blank line

        # prepare the table with no header or borders
        table = Table(show_header=False, box=None, pad_edge=True)
        table.add_column("Object", justify="right", style="bold")
        table.add_column("Placement", justify="left")

        spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
        for key, color in spheres:
            data = horoscope.get(key, {})

            if args.format == "names":
                obj_name = data.get("obj_name") or key
                placement = data.get("full") or "??"
            elif args.format == "glyphs":
                obj_name = data.get("obj_glyph") or key.upper()
                placement = data.get("glyph") or "??"
            elif args.format == "short":
                obj_name = data.get("obj_glyph") or key.upper()
                placement = data.get("short") or "??"
            else:
                obj_name = data.get("obj_glyph") or key.upper()
                placement = data.get("full") or "??"

            obj_name = str(obj_name)
            placement = str(placement)

            if colors and color:
                obj_name = colors.colorize(obj_name, color)

            table.add_row(obj_name, placement)

        console.print(Align.center(table))
