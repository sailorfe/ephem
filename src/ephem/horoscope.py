import swisseph as swe
from .constants import SIGNS, OBJECTS

SIGN_ORDER = list(SIGNS.keys())

def sign_from_index(index):
    """Returns zodiac sign name and its data for index 0-11 (Aries through Pisces)."""
    if not 0 <= index <=11:
        raise ValueError("Index must between 0 and 11 inclusive.")
    name = SIGN_ORDER[index]
    return name, SIGNS[name]


def get_planets(jd_now, jd_then):
    """Use swisseph to fetch planetary positions for day given from get_julian_day()."""
    planets = []
    planet_keys = [
        "ae", "ag", "hg", "cu", "fe", "sn", "pb",
        "ura", "nep", "plu", "mean_node", "true_node"
    ]
    # swe.calc_ut returns a list tuples with 6 values (longitude, latitude, distance, speed in lng, speed in lat, speed in dist.;); we only need longitude
    for planet_id, obj_key in enumerate(planet_keys):
        dd_now = swe.calc_ut(jd_now, planet_id)[0][0]
        dd_then = swe.calc_ut(jd_then, planet_id)[0][0]
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


def get_angles(jd_now, lat, lng):
    """Use swisseph to fetch ASC/MC. This specifies WSH (b'W'), but it truly doesn't matter (yet) because we're only printing two angles"""
    angles = []
    angle_keys = ["asc", "mc"]

    asc_mc = swe.houses(jd_now, lat, lng, b'W')[1]
    # swe.houses returns two tuples: house cusps (here WSH) and the 6-item list ascmc; we only need ASC/MC
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
    Build horoscope dictionary with data for location in DMS, different sign name formatting, sign qualities/elements for color schemes.
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

        # renderers called immediately to store strings:
        entry["full"] = f"{entry['deg']:>2} {entry['sign']} {entry['mnt']} {entry['sec']}{' r' if entry['rx'] else ''}"
        entry["short"] = f"{entry['deg']:>2} {entry['sign_trunc']} {entry['mnt']}{' r' if entry['rx'] else ''}"
        entry["glyph"] = f"{entry['deg']:>2} {entry['sign_glyph']} {entry['mnt']}{' r' if entry['rx'] else ''}"

        horoscope[body['obj_key']] = entry

    return horoscope
