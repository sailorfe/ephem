from .constants import GLYPHS, VERBOSE, Colors

def format_chart(args, title, lat, lng, dt, horoscope, planets, approx_time, approx_locale, config_locale):
    colors = Colors(use_color=not args.no_color)
    lines = []

    # -*- warnings + title -*-
    title = f"{title}\n{dt} UTC"

    if approx_time or approx_locale:
        title += f" hyp."

    warnings = []
    if approx_time:
        warnings.append("No time provided. Using UTC noon and not printing angles.\n")
    if approx_locale:
        warnings.append("No valid location provided or found in config. No angles will be printed.\n")
    if config_locale:
        warnings.append("Using location from config file.\n")

    for warning in warnings:
        lines.append(warning)  # or "italic", or however you're styling warnings

    if not args.no_coordinates and not approx_locale:
        geo_str = str(lat) + ", " + str(lng)
        title += f" @ {geo_str}"

    lines.append(colors.colorize(title, "bold"))

    # -*- filter objects -*-
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
        ("mc", None)
    ]

    if args.classical:
        spheres = [item for item in spheres if item[0] not in ("ura", "nep", "plu")]

    if approx_time or approx_locale or args.no_angles:
        spheres = [item for item in spheres if item[0] not in ("asc", "mc")]

    if args.node == "true":
        spheres = [item for item in spheres if item[0] != "mean_node"]
    else:
        spheres = [item for item in spheres if item[0] != "true_node"]


    for key, default_color in spheres:
        # fetch and format glyph
        if args.verbose:
            glyph = VERBOSE.get(key).ljust(12)
        else:
            glyph = GLYPHS.get(key, key.upper()).ljust(4)

        # fetch strings from horoscope
        if args.brief:
            placement = horoscope.get(key, {}).get("short", "??")
        else:
            placement = horoscope.get(key, {}).get("full", "??")

        # hg sect color
        if key == "hg":
            hg_lng = planets[2]['lng']
            ae_lng = planets[0]['lng']
            color = "red" if hg_lng < ae_lng else "blue"
        else:
            color = default_color

        line = f"{glyph} {placement}"

        if colors and color:
            line = colors.colorize(line, color)

        lines.append(line)

    return lines
