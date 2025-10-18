from rich.console import Console
from rich.table import Table
from rich.text import Text
from ephem.constants import AYANAMSAS, Colors


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


def get_time_data(dt_local, dt_utc):
    local_str = dt_local.strftime("%Y-%m-%d %H:%M:%S %Z")  # e.g. 2025-08-09 07:54 EDT
    utc_str = dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Show UTC only if it differs
    if local_str == utc_str:
        time_data = f"{local_str}"
    else:
        time_data = f"{local_str} | {utc_str}"

    return time_data


def get_geodata(lat, lng, args, approx_locale):
    # Show location if allowed
    no_geo = getattr(args, "no_geo", False)
    if not no_geo and not approx_locale:
        geodata = f"@ {lat}, {lng}"
    else:
        geodata = ""

    return geodata


def get_warnings(args, approx_time, approx_locale, config_locale):
    """Return warnings for incomplete data to display above chart."""
    warning_conditions = [
        (approx_time, "No time provided. Using UTC noon and not printing angles."),
        (
            approx_locale,
            "No valid location provided or found in config. No angles will be printed.",
        ),
        (config_locale and args.command == "cast", "Using location from config file."),
    ]
    return [msg for cond, msg in warning_conditions if cond]


def get_mercury_sect_color(planets, default_color):
    """Check if Mercury is diurnal or nocturnal for sect color scheme (default)."""
    try:
        hg_lng = planets[2]["lng"]  # hg index
        ae_lng = planets[0]["lng"]  # sun index
    except (IndexError, KeyError):
        return default_color
    return "red" if hg_lng < ae_lng else "blue"


def get_spheres(horoscope, args, planets, approx_time, approx_locale):
    """Assemble list of objects to display and their element/mode colors."""
    ELEMENT_COLORS = {
        "fire": "red",
        "earth": "green",
        "air": "bright_black",
        "water": "blue",
    }
    MODE_COLORS = {"cardinal": "magenta", "fixed": "yellow", "mutable": "cyan"}
    THEME_COLORS = {"element": ELEMENT_COLORS, "mode": MODE_COLORS, "sect": None}

    if args.theme == "sect":
        spheres = [
            ("ae", "bright_red"),
            ("ag", "bright_blue"),
            ("hg", None),
            ("cu", "blue"),
            ("fe", "blue"),
            ("sn", "red"),
            ("pb", "red"),
            ("ura", None),
            ("nep", None),
            ("plu", None),
            ("mean_node", None),
            ("true_node", None),
            ("asc", None),
            ("mc", None),
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


def get_houses_display(houses, args):
    """Assemble list of house cusps to display with element/mode colors."""
    ELEMENT_COLORS = {
        "fire": "red",
        "earth": "green",
        "air": "bright_black",
        "water": "blue",
    }
    MODE_COLORS = {"cardinal": "magenta", "fixed": "yellow", "mutable": "cyan"}

    house_list = []
    for house_data in houses:
        key = house_data.get("obj_key")

        if args.theme == "sect":
            # Houses don't have sect, so no color
            color = None
        elif args.theme == "element":
            color = ELEMENT_COLORS.get(house_data.get("trip"))
        elif args.theme == "mode":
            color = MODE_COLORS.get(house_data.get("quad"))
        else:
            color = None

        house_list.append((key, color, house_data))

    return house_list


def render_sphere_lines(spheres, horoscope, args, colors):
    lines = []
    for key, color in spheres:
        data = horoscope.get(key, {})

        if args.ascii:
            # ASCII mode: full names, abbreviated signs
            obj_name = data.get("obj_name", key).ljust(12)
            placement = f"{data.get('deg', 0):>2} {data.get('sign_trunc', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}{'r' if data.get('rx') else ''}"
        else:
            # Default: glyphs for objects, full sign names
            obj_name = data.get("obj_glyph", key.upper()).ljust(3)
            placement = f"{data.get('deg', 0):>2} {data.get('sign', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}{' r' if data.get('rx') else ''}"

        line = f"{obj_name} {placement}"
        if colors and color:
            line = colors.colorize(line, color)
        lines.append(line)
    return lines


def render_house_lines(houses, args, colors):
    """Render house cusp lines in ASCII format."""
    lines = []
    house_list = get_houses_display(houses, args)

    for key, color, data in house_list:
        if args.ascii:
            # ASCII mode: full names, abbreviated signs
            obj_name = key.ljust(12)
            placement = f"{data.get('deg', 0):>2} {data.get('trunc', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}"
        else:
            # Default: house number, full sign names
            obj_name = key.ljust(3)
            placement = f"{data.get('deg', 0):>2} {data.get('sign', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}"

        line = f"{obj_name} {placement}"
        if colors and color:
            line = colors.colorize(line, color)
        lines.append(line)

    return lines


console = Console()


def format_chart(
    args,
    title,
    lat,
    lng,
    dt_local,
    dt_utc,
    horoscope,
    planets,
    houses,
    hsys_name,
    approx_time,
    approx_locale,
    config_locale,
):
    offset = getattr(args, "offset", None)
    no_color = getattr(args, "no_color", False)

    """If --no-color, print bare chart; otherwise print Rich table."""
    if no_color:
        colors = Colors(False if args.no_color else True)
        lines = []

        # title + warnings
        lines.extend(get_warnings(args, approx_time, approx_locale, config_locale))
        lines.append(get_chart_title(title, approx_time, approx_locale, offset))
        lines.append(get_time_data(dt_local, dt_utc))
        lines.append(get_geodata(lat, lng, args, approx_locale))

        # body - planets/points
        spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
        lines.extend(render_sphere_lines(spheres, horoscope, args, colors))

        # houses
        if houses and not (approx_time or approx_locale or args.no_angles or args.no_houses):
            lines.extend(render_house_lines(houses, args, colors))

        return lines

    else:
        colors = Colors()
        # print warnings in yellow
        warnings = get_warnings(args, approx_time, approx_locale, config_locale)
        for warning in warnings:
            console.print(Text(warning, style="yellow"))

        chart_title = get_chart_title(title, approx_time, approx_locale, offset)

        time_data = get_time_data(dt_local, dt_utc)
        geodata = get_geodata(lat, lng, args, approx_locale)

        # Combine title and subtitle for table title
        full_title = f"{chart_title}\n{time_data}\n{geodata}"

        # Create main table with two columns and title
        main_table = Table(
            show_header=False,
            box=None,
            pad_edge=False,
            title=full_title,
            title_style="bold",
            title_justify="center",
        )
        main_table.add_column("Planets", justify="left")

        # Only add houses column if we have houses to display
        show_houses = houses and not (approx_time or approx_locale or args.no_angles or args.no_houses)
        if show_houses:
            main_table.add_column("Houses", justify="left")

        # Build planets table (left column)
        planets_table = Table(show_header=False, box=None, padding=(0, 1, 0, 1))
        if args.ascii:
            planets_table.add_column("Object", justify="left", style="bold")
        else:
            planets_table.add_column("Object", justify="right", style="bold")
        planets_table.add_column("Placement", justify="left")

        spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
        for key, color in spheres:
            data = horoscope.get(key, {})

            if args.ascii:
                # ASCII mode: full names, abbreviated signs
                obj_name = data.get("obj_name") or key
                placement = f"{data.get('deg', 0):>2} {data.get('sign_trunc', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}{' r' if data.get('rx') else ''}"
            else:
                # Default: glyphs for objects, full sign names
                obj_name = data.get("obj_glyph") or key.upper()
                placement = f"{data.get('deg', 0):>2} {data.get('sign', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}{' r' if data.get('rx') else ''}"

            # Apply color using Rich Text object
            if color:
                obj_name = Text(str(obj_name), style=color)
            else:
                obj_name = Text(str(obj_name))

            planets_table.add_row(obj_name, placement)

        # Build houses table (right column) if applicable
        if show_houses:
            houses_table = Table(show_header=False, box=None, padding=(0, 1, 0, 1), title=hsys_name)
            if args.ascii:
                houses_table.add_column("House", justify="left", style="bold")
            else:
                houses_table.add_column("House", justify="right", style="bold")
            houses_table.add_column("Cusp", justify="left")

            house_list = get_houses_display(houses, args)
            for key, color, data in house_list:
                if args.ascii:
                    obj_name = key
                    placement = f"{data.get('deg', 0):>2} {data.get('trunc', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}"
                else:
                    obj_name = key
                    placement = f"{data.get('deg', 0):>2} {data.get('sign', '???')} {data.get('mnt', 0):02d} {data.get('sec', 0):02d}"

                # Apply color to obj_name using Rich Text object
                if color:
                    obj_name = Text(obj_name, style=color)
                else:
                    obj_name = Text(obj_name)

                houses_table.add_row(obj_name, placement)

            main_table.add_row(planets_table, houses_table)
        else:
            main_table.add_row(planets_table)

        console.print(main_table)
