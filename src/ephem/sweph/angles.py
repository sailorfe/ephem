import swisseph as swe
from ephem.utils.signs import sign_from_index
from .ayanamsas import get_calc_flag


def get_angles(jd_now, lat, lng, offset=None):
    calc_flag = get_calc_flag(offset)
    angles = []
    angle_keys = ["asc", "mc"]

    # use houses_ex to pass calc_flag for sidereal if needed
    asc_mc = swe.houses_ex(jd_now, lat, lng, b"W", calc_flag)[1]

    for angle_val, obj_key in zip(asc_mc[:2], angle_keys):
        dms = swe.split_deg(angle_val, 8)
        sign_name, sign_data = sign_from_index(dms[4])
        angles.append(
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
                "lng": asc_mc[0],
            }
        )

    return angles
