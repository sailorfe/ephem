from datetime import datetime,timezone
import swisseph as swe
from constants import GLYPHS, VERBOSE, Colors

def jd_to_datetime(jd_now):
    y, m, d, h = swe.revjul(jd_now)
    hours = int(h)
    minutes = int((h - hours) * 60)
    seconds = int(((h - hours) * 60 - minutes) * 60)
    dt = datetime(y, m, d, hours, minutes, seconds, tzinfo=timezone.utc)
    return datetime.strftime(dt, "%Y-%m-d %H:%M")

def print_chart(args, lat, lng, dt, horoscope, planets):
    colors = Colors(use_color=not args.no_color)

    if args.command == "chart" and args.title:
        title = f"{args.title}\n{dt} UTC"
    else:
        title = f"{dt} UTC"

    if args.command == "chart" and (args.time is None):
        title += f" hyp."

    if not args.no_geo:
        geo_str = str(lat) + ", " + str(lng)
        title += f"\n@ {geo_str}"

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

    if args.command == "chart" and (args.noon or args.zero):
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

        line = f"{glyph} {placement}"

        if colors and color:
            line = colors.colorize(line, color)

        print(line)
