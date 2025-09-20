import swisseph as swe
from ephem.utils.signs import sign_from_index
from .ayanamsas import get_calc_flag

PLANET_KEYS = [
    "ae",
    "ag",
    "hg",
    "cu",
    "fe",
    "sn",
    "pb",
    "ura",
    "nep",
    "plu",
    "mean_node",
    "true_node",
]


def get_planets(jd_now, jd_then, offset=None):
    """
    Fetch planetary positions using Swiss Ephemeris.
    jd_now: current Julian day
    jd_then: previous/next Julian day (for retrograde)
    offset: None = tropical, int = sidereal ayanamsha index
    """
    calc_flag = get_calc_flag(offset)
    planets = []

    for planet_id, obj_key in enumerate(PLANET_KEYS):
        dd_now = swe.calc_ut(jd_now, planet_id, calc_flag)[0][0]
        dd_then = swe.calc_ut(jd_then, planet_id, calc_flag)[0][0]

        dms = swe.split_deg(dd_now, 8)
        sign_name, sign_data = sign_from_index(dms[4])

        planets.append(
            {
                "obj_key": obj_key,
                "deg": dms[0],
                "mnt": dms[1],
                "sec": dms[2],
                "sign": sign_name,
                "trunc": sign_data["trunc"],
                "glyph": sign_data["glyph"],
                "trip": sign_data["trip"],
                "quad": sign_data["quad"],
                "rx": dd_then > dd_now,
                "lng": dd_now,
            }
        )

    return planets
