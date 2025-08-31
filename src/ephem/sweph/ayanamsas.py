import swisseph as swe
from ephem.constants import AYANAMSAS


def get_calc_flag(offset):
    """
    Return Swiss Ephemeris calculation flag including sidereal mode if requested.
    offset: None = tropical, int = sidereal ayanamsha index
    """
    calc_flag = swe.FLG_SWIEPH

    if offset is None:
        return calc_flag

    try:
        sid_mode = list(AYANAMSAS.values())[offset]
    except IndexError:
        raise ValueError(f"Sidereal offset index out of range: {offset}")

    swe.set_sid_mode(sid_mode, 0, 0)
    calc_flag |= swe.FLG_SIDEREAL
    return calc_flag
