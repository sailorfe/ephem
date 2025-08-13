import swisseph as swe
from ephem.constants import SIGNS, AYANAMSAS
from ephem.utils.locale import get_locale
from datetime import datetime, timezone

SIGN_ORDER = list(SIGNS.keys())

def sign_from_index(index):
    name = SIGN_ORDER[index]
    return name, SIGNS[name]

def _get_calc_flag(offset):
    calc_flag = swe.FLG_SWIEPH
    if offset is None:
        return calc_flag  # Tropical
    try:
        sid_mode = list(AYANAMSAS.values())[int(offset)]
    except (IndexError, ValueError):
        raise ValueError(f"Sidereal offset index out of range: {offset}")
    swe.set_sid_mode(sid_mode, 0, 0)
    calc_flag |= swe.FLG_SIDEREAL
    return calc_flag

def run(args):
    lat, lng, approx_locale, *_ = get_locale(args)
    offset = getattr(args, 'offset', None)  # Get offset from args

    now = datetime.now(timezone.utc)
    jd = swe.julday(
        now.year,
        now.month,
        now.day,
        now.hour + now.minute / 60 + now.second / 3600
    )

    calc_flag = _get_calc_flag(offset)
    # houses_ex allows passing calc_flag for sidereal
    houses = swe.houses_ex(jd, lat, lng, b'W', calc_flag)
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

