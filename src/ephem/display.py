from .constants import Colors

def get_chart_title(title, dt, lat, lng, args, approx_time, approx_locale):
    # return formatted cargshart title string
    if title is None:
        title = ""
    title_str = f"{title}\n{dt} UTC"
    if approx_time or approx_locale:
        title_str += " hyp."
    if not args.no_coordinates and not approx_locale:
        title_str += f" @ {lat}, {lng}"
    return title_str


def get_warnings(args, approx_time, approx_locale, config_locale):
    # return a list of warning messages to display above chart
    warning_conditions = [
        (approx_time, "No time provided. Using UTC noon and not printing angles."),
        (approx_locale, "No valid location provided or found in config. No angles will be printed."),
        (config_locale and args.command == "cast", "Using location from config file.")
    ]
    return [msg for cond, msg in warning_conditions if cond]


def get_mercury_sect_color(planets, default_color):
    try:
        hg_lng = planets[2]['lng']
        ae_lng = planets[0]['lng']
    except (IndexError, KeyError):
        return default_color
    return "red" if hg_lng < ae_lng else "blue"


def get_spheres(horoscope, args, planets, approx_time, approx_locale):
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


def format_chart(args, title, lat, lng, dt, horoscope, planets, approx_time, approx_locale, config_locale):
    colors = Colors(use_color=not args.no_color)
    lines = []

    # title + warnings
    lines.extend(get_warnings(args, approx_time, approx_locale, config_locale))
    lines.append(colors.colorize(get_chart_title(title, dt, lat, lng, args, approx_time, approx_locale), "bold"))

    # body
    spheres = get_spheres(horoscope, args, planets, approx_time, approx_locale)
    lines.extend(render_sphere_lines(spheres, horoscope, args, colors))

    return lines
