import swisseph as swe
from ephem.constants import SIGNS
from ephem.utils import get_locale
from datetime import datetime, timezone

SIGN_ORDER = list(SIGNS.keys())

def sign_from_index(index):
    name = SIGN_ORDER[index]
    return name, SIGNS[name]

def run(args):
    lat, lng, approx_locale, *_ = get_locale(args)

    now = datetime.now(timezone.utc)
    jd = swe.julday(
        now.year,
        now.month,
        now.day,
        now.hour + now.minute / 60 + now.second / 3600
    )
    # houses() returns two tuples: house cusps and array ascmc; we only need asc index 0 of the 2nd
    houses = swe.houses(jd, lat, lng, b'W')
    asc_deg = houses[1][0]
    dms = swe.split_deg(asc_deg, 8)
    _, sign_data = sign_from_index(dms[4])

    if args.glyphs:
        sign_display = sign_data['glyph']
    else:
        sign_display = sign_data['trunc']

    if approx_locale:
        print("No location given or found in config; using Null Island (0,0).")

    print(f"AC {dms[0]:>2} {sign_display} {dms[1]}")

