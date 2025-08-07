from constants import GLYPHS, Colors

def print_chart(args, date_str, time_str, horoscope, planets):
    colors = Colors(use_color=not args.no_color)

    if args.title:
        title = f"{args.title}\n{date_str} {time_str} UTC"
    else:
        title = f"{date_str} {time_str} UTC"

    if args.command == "chart" and args.event and args.approximate:
        title += f" hyp."

    print(colors.colorize(title, "bold"))

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

    if args.command == "chart" and args.event and args.approximate:
        spheres = [item for item in spheres if item[0] not in ("asc", "mc")]

    if args.node == "true":
        spheres = [item for item in spheres if item[0] != "mean_node"]
    else:
        spheres = [item for item in spheres if item[0] != "true_node"]


    for key, default_color in spheres:
        # fetch and format glyph
        glyph = GLYPHS.get(key, key.upper())

        # fetch strings from horoscope
        if args.short:
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

        line = f"{glyph:<4} {placement}"

        if colors and color:
            line = colors.colorize(line, color)

        print(line)
