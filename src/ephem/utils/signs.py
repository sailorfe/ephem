from ephem.constants import SIGNS

SIGN_ORDER = list(SIGNS.keys())


def sign_from_index(index):
    """Return zodiac sign name and its data for index 0-11 (Aries through Pisces)."""
    if not 0 <= index <= 11:
        raise ValueError("Index must be between 0 and 11 inclusive.")
    name = SIGN_ORDER[index]
    return name, SIGNS[name]
