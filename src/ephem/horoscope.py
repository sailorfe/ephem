import swisseph as swe
from .constants import SIGNS, OBJECTS, AYANAMSAS

SIGN_ORDER = list(SIGNS.keys())


def sign_from_index(index):
    """Return zodiac sign name and its data for index 0-11 (Aries through Pisces)."""
    if not 0 <= index <= 11:
        raise ValueError("Index must be between 0 and 11 inclusive.")
    name = SIGN_ORDER[index]
    return name, SIGNS[name]


def _get_calc_flag(offset):
    """
    Return Swiss Ephemeris calculation flag including sidereal mode if requested.
    offset: None = tropical, int = sidereal ayanamsha index
    """
    calc_flag = swe.FLG_SWIEPH

    if offset is None:
        return calc_flag  # Tropical

    try:
        sid_mode = list(AYANAMSAS.values())[offset]
    except IndexError:
        raise ValueError(f"Sidereal offset index out of range: {offset}")

    swe.set_sid_mode(sid_mode, 0, 0)
    calc_flag |= swe.FLG_SIDEREAL
    return calc_flag


PLANET_KEYS = [
    "ae", "ag", "hg", "cu", "fe", "sn", "pb",
    "ura", "nep", "plu", "mean_node", "true_node"
]


def get_planets(jd_now, jd_then, offset=None):
    """
    Fetch planetary positions using Swiss Ephemeris.
    jd_now: current Julian day
    jd_then: previous/next Julian day (for retrograde)
    offset: None = tropical, int = sidereal ayanamsha index
    """
    calc_flag = _get_calc_flag(offset)
    planets = []

    for planet_id, obj_key in enumerate(PLANET_KEYS):
        dd_now = swe.calc_ut(jd_now, planet_id, calc_flag)[0][0]
        dd_then = swe.calc_ut(jd_then, planet_id, calc_flag)[0][0]

        dms = swe.split_deg(dd_now, 8)
        sign_name, sign_data = sign_from_index(dms[4])

        planets.append({
            'obj_key': obj_key,
            'deg': dms[0],
            'mnt': dms[1],
            'sec': dms[2],
            'sign': sign_name,
            'trunc': sign_data['trunc'],
            'glyph': sign_data['glyph'],
            'trip': sign_data['trip'],
            'quad': sign_data['quad'],
            'rx': dd_then > dd_now,
            'lng': dd_now
        })

    return planets


def get_angles(jd_now, lat, lng, offset=None):
    """Fetch ASC and MC for given date and location, optionally in sidereal mode."""
    calc_flag = _get_calc_flag(offset)
    angles = []
    angle_keys = ["asc", "mc"]

    # Use houses_ex to pass calc_flag for sidereal if needed
    asc_mc = swe.houses_ex(jd_now, lat, lng, b'W', calc_flag)[1]

    for angle_val, obj_key in zip(asc_mc[:2], angle_keys):
        dms = swe.split_deg(angle_val, 8)
        sign_name, sign_data = sign_from_index(dms[4])
        angles.append({
            'obj_key': obj_key,
            'deg': dms[0],
            'mnt': dms[1],
            'sec': dms[2],
            'sign': sign_name,
            'trunc': sign_data['trunc'],
            'glyph': sign_data['glyph'],
            'trip': sign_data['trip'],
            'quad': sign_data['quad']
        })

    return angles


def build_horoscope(planets, angles):
    """
    Build horoscope dictionary with data for location in DMS,
    including sign qualities/elements and retrograde info.
    """
    horoscope = {}
    all_bodies = planets + angles

    for body in all_bodies:
        obj_data = OBJECTS[body['obj_key']]

        entry = {
            "obj_name": obj_data['name'],
            "obj_glyph": obj_data['glyph'],
            "deg": body['deg'],
            "mnt": body['mnt'],
            "sec": body['sec'],
            "sign": body['sign'],
            "sign_trunc": body['trunc'],
            "sign_glyph": body['glyph'],
            "trip": body['trip'],
            "quad": body['quad'],
            "rx": body.get('rx', False),
        }

        # pre-rendered strings for display
        entry["full"] = f"{entry['deg']:>2} {entry['sign']} {entry['mnt']} {entry['sec']}{' r' if entry['rx'] else ''}"
        entry["short"] = f"{entry['deg']:>2} {entry['sign_trunc']} {entry['mnt']}{' r' if entry['rx'] else ''}"
        entry["glyph"] = f"{entry['deg']:>2} {entry['sign_glyph']} {entry['mnt']}{' r' if entry['rx'] else ''}"

        horoscope[body['obj_key']] = entry

    return horoscope
