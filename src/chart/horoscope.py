import swisseph as swe
from .constants import SIGNS, OBJECTS

SIGN_ORDER = list(SIGNS.keys())

def sign_from_index(index):
    name = SIGN_ORDER[index % 12]
    return name, SIGNS[name]

def get_planets(jd_now, jd_then):
    planets = []
    planet_keys = [
        "ae", "ag", "hg", "cu", "fe", "sn", "pb",
        "ura", "nep", "plu", "mean_node", "true_node"
    ]

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
            'rx': dd_then > dd_now
        })
    return planets

def get_angles(jd_now, lat, lng):
    angles = []
    angle_keys = ["asc", "mc"]
    asc_mc = swe.houses(jd_now, lat, lng, b'W')[1]
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
    horoscope = {}
    all_bodies = planets + angles

    for body in all_bodies:
        obj_data = OBJECTS[body['obj_key']]

        # Core data
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

        # Renderers called immediately to store strings:
        entry["full"] = f"{entry['deg']} {entry['sign']} {entry['mnt']} {entry['sec']}{' r' if entry['rx'] else ''}"
        entry["short"] = f"{entry['deg']} {entry['sign_trunc']} {entry['mnt']}{' r' if entry['rx'] else ''}"
        entry["glyph"] = f"{entry['deg']} {entry['sign_glyph']} {entry['mnt']}{' r' if entry['rx'] else ''}"

        horoscope[body['obj_key']] = entry

    return horoscope
