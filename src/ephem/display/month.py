from datetime import datetime
from rich.console import Console
from rich.table import Table, box
from rich.align import Align
from rich.text import Text
from ephem.constants import OBJECTS, AYANAMSAS
from ephem.sweph import get_planets, build_horoscope
from ephem.utils.signs import sign_from_index
from ephem.utils.year import validate_year
import swisseph as swe


def get_sidereal_time(jd):
    gst = swe.sidtime(jd) % 24
    total_seconds = int(round(gst * 3600))
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_moon_positions(jd_midnight, jd_noon, offset=None, ascii_mode=False):
    calc_flag = swe.FLG_SWIEPH
    if offset is not None:
        try:
            sid_mode = list(AYANAMSAS.values())[offset]
            swe.set_sid_mode(sid_mode, 0, 0)
            calc_flag |= swe.FLG_SIDEREAL
        except IndexError:
            pass

    moon_0hr = swe.calc_ut(jd_midnight, 1, calc_flag)[0][0]
    moon_noon = swe.calc_ut(jd_noon, 1, calc_flag)[0][0]

    def format_moon_pos(lng):
        dms = swe.split_deg(lng, 8)
        _, sign_data = sign_from_index(dms[4])
        if ascii_mode:
            return f"{dms[0]:2d} {sign_data['trunc']:<3} {dms[1]:02d} {dms[2]:02d}"
        else:
            return f"{dms[0]:2d} {sign_data['glyph']:<3} {dms[1]:02d} {dms[2]:02d}"

    return format_moon_pos(moon_0hr), format_moon_pos(moon_noon)


def format_planet_position(entry, ascii_mode=False):
    deg_str = f"{entry['deg']:2d}"
    mnt_str = f"{entry['mnt']:02d}"
    sec_str = f"{entry.get('sec', 0):02d}"
    rx_str = " r" if entry.get("rx") else ""

    if ascii_mode:
        sign_str = f"{entry['sign_trunc']:<3}"
    else:
        sign_str = f"{entry['sign_glyph']:<3}"

    return f"{deg_str} {sign_str} {mnt_str} {sec_str}{rx_str}"


def format_calendar(args):
    validate_year(args.year)

    offset = getattr(args, "offset", None)
    ascii_mode = getattr(args, "ascii", False)

    first_day = datetime(args.year, args.month, 1)
    next_month = (
        datetime(args.year + 1, 1, 1)
        if args.month == 12
        else datetime(args.year, args.month + 1, 1)
    )
    days_in_month = (next_month - first_day).days

    console = Console()
    month_name = first_day.strftime("%B %Y")
    subtitle = "Tropical"
    if offset is not None:
        try:
            ayanamsa_name = list(AYANAMSAS.keys())[offset]
            subtitle = f"Sidereal — {ayanamsa_name}"
        except IndexError:
            subtitle = f"Sidereal — Offset {offset}"

    title_line = month_name
    if subtitle:
        title_line += f" — {subtitle}"

    console.print(Align.center(Text(f"{title_line}", style="bold")))

    EPHEMERIS_COLUMNS = [
        ("Day", "right", "bold"),
        ("Sid. 0hr", "center", None),
        ("ae", "left", None),  # Sun
        ("ag", "left", None),  # Moon (0hr)
        ("ag_noon", "left", None),  # Moon (noon)
        ("true_node", "left", None),
        ("hg", "left", None),  # Mercury
        ("cu", "left", None),  # Venus
        ("fe", "left", None),  # Mars
        ("sn", "left", None),  # Jupiter
        ("pb", "left", None),  # Saturn
        ("ura", "left", None),  # Uranus
        ("nep", "left", None),  # Neptune
        ("plu", "left", None),  # Pluto
    ]

    table = Table(show_header=True, box=box.SQUARE)
    for col_name, cell_justify, style in EPHEMERIS_COLUMNS:
        if col_name == "ag":
            header_str = "0hr Moon" if ascii_mode else "0hr " + OBJECTS["ag"]["glyph"]
        elif col_name == "ag_noon":
            header_str = "Noon Moon" if ascii_mode else "Noon " + OBJECTS["ag"]["glyph"]
        elif col_name in OBJECTS:
            if ascii_mode:
                header_str = OBJECTS[col_name]["name"]
            else:
                header_str = OBJECTS[col_name]["glyph"]
        else:
            header_str = col_name
        table.add_column(
            Text(header_str, justify="center"),
            justify=cell_justify,
            style=style,
            no_wrap=True,
        )

    day_abbrevs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    for day in range(1, days_in_month + 1):
        current_date = datetime(args.year, args.month, day)
        day_abbrev = day_abbrevs[current_date.weekday()]

        jd_midnight = swe.julday(args.year, args.month, day, 0.0)
        jd_noon = swe.julday(args.year, args.month, day, 12.0)
        jd_prev = jd_midnight - 1 / 1440

        sid_time = get_sidereal_time(jd_midnight)
        planets = get_planets(jd_midnight, jd_prev, offset)
        horoscope = build_horoscope(planets, [], [])

        moon_0hr, moon_noon = get_moon_positions(
            jd_midnight, jd_noon, offset, ascii_mode=ascii_mode
        )

        day_str = f"{day:2d} {day_abbrev}"

        row_data = [day_str, sid_time]
        for col_name, _, _ in EPHEMERIS_COLUMNS[2:]:
            if col_name == "ag":
                row_data.append(moon_0hr)
            elif col_name == "ag_noon":
                row_data.append(moon_noon)
            elif col_name in horoscope:
                row_data.append(
                    format_planet_position(horoscope[col_name], ascii_mode=ascii_mode)
                )
            else:
                row_data.append("--")

        table.add_row(*row_data)

    console.print(Align.center(table))
    return None
