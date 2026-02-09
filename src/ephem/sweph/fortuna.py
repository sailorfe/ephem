import swisseph as swe
from ephem.utils.signs import sign_from_index
from ephem.constants import OBJECTS, SIGNS
from ephem.models import Position


def get_pars_fortunae(angles, planets):
    ascendant = angles[0].lng
    sun = planets[0].lng
    moon = planets[1].lng

    # determine sect
    if ascendant > sun:
        raw_fortuna = ascendant + moon - sun
    else:
        raw_fortuna = ascendant - moon + sun

    # normalize to 0-360 range
    fortuna = raw_fortuna % 360

    dms = swe.split_deg(fortuna, 8)
    sign_name, _ = sign_from_index(dms[4])

    position = Position(
        obj=OBJECTS["for"],
        sign=SIGNS[sign_name],
        deg=dms[0],
        mnt=dms[1],
        sec=dms[2],
        rx=False,  # Part of Fortune doesn't retrograde
    )
    position.lng = fortuna

    return [position]
