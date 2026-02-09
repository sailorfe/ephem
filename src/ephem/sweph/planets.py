import swisseph as swe
from ephem.utils.signs import sign_from_index
from ephem.constants import OBJECTS, SIGNS
from ephem.models import Position
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
    calc_flag = get_calc_flag(offset)
    positions = []

    for planet_id, obj_key in enumerate(PLANET_KEYS):
        dd_now = swe.calc_ut(jd_now, planet_id, calc_flag)[0][0]
        dd_then = swe.calc_ut(jd_then, planet_id, calc_flag)[0][0]
        dms = swe.split_deg(dd_now, 8)

        sign_name, _ = sign_from_index(dms[4])

        position = Position(
            obj=OBJECTS[obj_key],
            sign=SIGNS[sign_name],
            deg=dms[0],
            mnt=dms[1],
            sec=dms[2],
            rx=dd_then > dd_now,
        )
        position.lng = dd_now

        positions.append(position)

    return positions
