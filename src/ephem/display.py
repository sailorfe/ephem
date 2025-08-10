from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text
from .constants import Colors

def get_chart_title(title, approx_time, approx_locale):
    """Fetches given chart title from `cast [event]` argument or defaults to none"""
    if title is None:
        title = ""
    title_str = f"{title}"
    if approx_time or approx_locale:
        title_str += " hyp."
    return title_str


def get_chart_subtitle(dt, lat, lng, args, approx_locale):
    """Fetch subtitle from date and location."""
    subtitle_str = f"{dt} UTC"
    if not args.no_coordinates and not approx_locale:
        subtitle_str += f" @ {lat} {lng}"
    return subtitle_str


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
        elif args.format == "mixed":
            obj_name = data.get("obj_glyph", key.upper()).ljust(6)
            placement = data.get("full", "??")

        line = f"{obj_name} {placement}"
        if colors and color:
            line = colors.colorize(line, color)
        lines.append(line)
    return lines


console = Console()

def format_chart(args, title, lat, lng, dt, horoscope, planets, approx_time, approx_locale, config_locale):
    """If --no-color, print bare chart; otherwise print Rich table."""
    if args.no_color:
        # i'm not convinced i need this but there is a loose function somehwere that expects 4 arguments
        colors = Colors(False if args.no_color else True)
        lines = []

        # title + warnings
        lines.extend(get_warnings(args, approx_time, approx_locale, config_locale))
        lines.append(get_chart_title(title, approx_time, approx_locale))
        lines.append(get_chart_subtitle(dt, lat, lng, args, approx_locale))

        # body
        spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
                                                                   # what is this colors doing here!!
        lines.extend(render_sphere_lines(spheres, horoscope, args, colors))

        return lines
    else:
        colors=Colors()
        # print warnings in yellow
        warnings = get_warnings(args, approx_time, approx_locale, config_locale)
        for warning in warnings:
            console.print(Text(warning, style="yellow"))

        # centered bold title
        chart_title = get_chart_title(title, approx_time, approx_locale)
        chart_subtitle = get_chart_subtitle(dt, lat, lng, args, approx_locale)
        console.print(Align.center(Text(chart_title, style="bold")))
        console.print(Align.center(Text(chart_subtitle, style="bold")))
        console.print()  # Blank line

        # prepare the table with no header or borders
        table = Table(show_header=False, box=None, pad_edge=True)
        table.add_column("Object", justify="right", style="bold")
        table.add_column("Placement", justify="left")

        spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
        for key, color in spheres:
            data = horoscope.get(key, {})

            # Use safe fallback values for name and position
            if args.format == "names":
                obj_name = data.get("obj_name") or key
                placement = data.get("full") or "??"
            elif args.format == "glyphs":
                obj_name = data.get("obj_glyph") or key.upper()
                placement = data.get("glyph") or "??"
            elif args.format == "short":
                obj_name = data.get("obj_glyph") or key.upper()
                placement = data.get("short") or "??"
            elif args.format == "mixed":
                obj_name = data.get("obj_glyph") or key.upper()
                placement = data.get("full") or "??"
            else:
                obj_name = data.get("obj_name") or key
                placement = data.get("full") or "??"

            # ensure these are strings (not None or other types)
            obj_name = str(obj_name)
            placement = str(placement)

            # colorize only if color is not None and colors are enabled
            if colors and color:
                obj_name = colors.colorize(obj_name, color)

            table.add_row(obj_name, placement)

        console.print(Align.center(table))
