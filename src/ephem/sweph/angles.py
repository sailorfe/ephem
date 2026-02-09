import swisseph as swe
from ephem.constants import SIGNS, OBJECTS
from ephem.models import Position
from ephem.utils.signs import sign_from_index
from .ayanamsas import get_calc_flag


def get_angles(jd_now, lat, lng, offset=None):
    calc_flag = get_calc_flag(offset)
    angle_keys = ["asc", "mc"]

    # use houses_ex to pass calc_flag for sidereal if needed
    asc_mc = swe.houses_ex(jd_now, lat, lng, b"W", calc_flag)[1]

    positions = []
    for idx, (angle_val, obj_key) in enumerate(zip(asc_mc[:2], angle_keys)):
        dms = swe.split_deg(angle_val, 8)
        sign_name, _ = sign_from_index(dms[4])

        position = Position(
            obj=OBJECTS[obj_key],
            sign=SIGNS[sign_name],
            deg=dms[0],
            mnt=dms[1],
            sec=dms[2],
            rx=False,
        )
        # store the actual longitude for this angle
        position.lng = angle_val

        positions.append(position)

    return positions
