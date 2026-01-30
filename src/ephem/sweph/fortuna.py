import swisseph as swe
from ephem.utils.signs import sign_from_index

def get_pars_fortunae(angles, planets):
    ascendant = angles[0]["lng"]
    sun = planets[0]["lng"]
    moon = planets[1]["lng"]

    # determine sect
    if ascendant > sun:
        raw_fortuna = ascendant + moon - sun
    else:
        raw_fortuna = ascendant - moon + sun

    # normalize
    if raw_fortuna > 360.0:
        fortuna = raw_fortuna - 360.0
    else:
        fortuna = raw_fortuna

    dms = swe.split_deg(fortuna, 8)
    sign_name, sign_data = sign_from_index(dms[4])

    part_of_fortune = []
    part_of_fortune.append(
            {
            "obj_key": "for",
            "deg": dms[0],
            "mnt": dms[1],
            "sec": dms[2],
            "sign": sign_name,
            "trunc": sign_data["trunc"],
            "glyph": sign_data["glyph"],
            "trip": sign_data["trip"],
            "quad": sign_data["quad"],
            "lng": fortuna,
            }
            )

    return part_of_fortune
