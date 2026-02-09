import swisseph as swe
from ephem.models import Sign, CelestialObject

SIGNS = {
    "Aries": Sign("Aries", "Ari", "♈︎", "fire", "cardinal"),
    "Taurus": Sign("Taurus", "Tau", "♉︎", "earth", "fixed"),
    "Gemini": Sign("Gemini", "Gem", "♊︎", "air", "mutable"),
    "Cancer": Sign("Cancer", "Can", "♋︎", "water", "cardinal"),
    "Leo": Sign("Leo", "Leo", "♌︎", "fire", "fixed"),
    "Virgo": Sign("Virgo", "Vir", "♍︎", "earth", "mutable"),
    "Libra": Sign("Libra", "Lib", "♎︎", "air", "cardinal"),
    "Scorpio": Sign("Scorpio", "Sco", "♏︎", "water", "fixed"),
    "Sagittarius": Sign("Sagittarius", "Sag", "♐︎", "fire", "mutable"),
    "Capricorn": Sign("Capricorn", "Cap", "♑︎", "earth", "cardinal"),
    "Aquarius": Sign("Aquarius", "Aqu", "♒︎", "air", "fixed"),
    "Pisces": Sign("Pisces", "Pis", "♓︎", "water", "mutable"),
}


OBJECTS = {
    "ae": CelestialObject("ae", "Sun", "☉"),
    "ag": CelestialObject("ag", "Moon", "☽"),
    "hg": CelestialObject("hg", "Mercury", "☿"),
    "cu": CelestialObject("cu", "Venus", "♀"),
    "fe": CelestialObject("fe", "Mars", "♂"),
    "sn": CelestialObject("sn", "Jupiter", "♃"),
    "pb": CelestialObject("pb", "Saturn", "♄"),
    "for": CelestialObject("for", "Part of Fortune", "🝴"),
    "ura": CelestialObject("ura", "Uranus", "♅"),
    "nep": CelestialObject("nep", "Neptune", "♆"),
    "plu": CelestialObject("plu", "Pluto", "♇"),
    "mean_node": CelestialObject("mean_node", "Mean Node", "M☊"),
    "true_node": CelestialObject("true_node", "True Node", "T☊"),
    "asc": CelestialObject("asc", "Ascendant", "AC"),
    "mc": CelestialObject("mc", "Midheaven", "MC"),
}

AYANAMSAS = {
    "Fagan-Bradley": swe.SIDM_FAGAN_BRADLEY,  # 0
    "Lahiri": swe.SIDM_LAHIRI,  # 1
    "Deluce": swe.SIDM_DELUCE,  # 2
    "Raman": swe.SIDM_RAMAN,  # 3
    "Ushashashi": swe.SIDM_USHASHASHI,  # 4
    "Krishnamurti": swe.SIDM_KRISHNAMURTI,  # 5
    "Djwhal Khul": swe.SIDM_DJWHAL_KHUL,  # 6
    "Yukteshwar": swe.SIDM_YUKTESHWAR,  # 7
    "J.N. Bhasin": swe.SIDM_JN_BHASIN,  # 8
    "Babylonian/Kugler 1": swe.SIDM_BABYL_KUGLER1,  # 9
    "Babylonian/Kugler 2": swe.SIDM_BABYL_KUGLER2,  # 10
    "Babylolnian/Kugler 3": swe.SIDM_BABYL_KUGLER3,  # 11
    "Babylonian/Huber": swe.SIDM_BABYL_HUBER,  # 12
    "Babylonian/Eta Piscium": swe.SIDM_BABYL_ETPSC,  # 13
    "Babylonian/Aldebaran = 15 Tau": swe.SIDM_ALDEBARAN_15TAU,  # 14
    "Hipparchos": swe.SIDM_HIPPARCHOS,  # 15
    "Sassanian": swe.SIDM_SASSANIAN,  # 16
    "Galact. Center = 0 Sag": swe.SIDM_GALCENT_0SAG,  # 17
    "J2000": swe.SIDM_J2000,  # 18
    "J1900": swe.SIDM_J1900,  # 19
    "B1950": swe.SIDM_B1950,  # 20
    "Suryasiddhanta": swe.SIDM_SURYASIDDHANTA,  # 21
    "Suryasiddhanta, mean Sun": swe.SIDM_SURYASIDDHANTA_MSUN,  # 22
    "Aryabhata": swe.SIDM_ARYABHATA,  # 23
    "Aryabhata, mean Sun": swe.SIDM_ARYABHATA_MSUN,  # 24
    "SS Revati": swe.SIDM_SS_REVATI,  # 25
    "SS Citra": swe.SIDM_SS_CITRA,  # 26
    "True Citra": swe.SIDM_TRUE_CITRA,  # 27
    "True Revati": swe.SIDM_TRUE_REVATI,  # 28
    "True Pusya (PVRN Rao)": swe.SIDM_TRUE_PUSHYA,  # 29
    "Galactic Center (Gil Brand)": swe.SIDM_GALCENT_RGILBRAND,  # 30
    "Galactic Equator (IAU1958)": swe.SIDM_GALEQU_IAU1958,  # 31
    "Galactic Equator": swe.SIDM_GALEQU_TRUE,  # 32
    "Galactic Equator mid-Mula": swe.SIDM_GALEQU_MULA,  # 33
    "Skydram (Mardysk)": swe.SIDM_GALALIGN_MARDYKS,  # 34
    "True Mula (Chanda Hari)": swe.SIDM_TRUE_MULA,  # 35
    "Dhruva/Gal. Center/Mula (Wilhelm)": swe.SIDM_GALCENT_MULA_WILHELM,  # 36
    "Aryabhata 522": swe.SIDM_ARYABHATA_522,  # 37
    "Babylonian/Britton": swe.SIDM_BABYL_BRITTON,  # 38
    "'Vedic'/Sheoran": swe.SIDM_TRUE_SHEORAN,  # 39
    "Cochrane (Gal. Center = 0 Cap)": swe.SIDM_GALCENT_COCHRANE,  # 40
    "Galactic Equator (Forenza)": swe.SIDM_GALEQU_FIORENZA,  # 41
    "Vettius Valens": swe.SIDM_VALENS_MOON,  # 42
    "Lahiri 1940": swe.SIDM_LAHIRI_1940,  # 43
    "Lahiri VP285": swe.SIDM_LAHIRI_VP285,  # 44
    "Krishnamurti-Senthilathiban": swe.SIDM_KRISHNAMURTI_VP291,  # 45
    "Lahiri ICRC": swe.SIDM_LAHIRI_ICRC,  # 46
}


class Colors:
    def __init__(self, use_color=True):
        self.use_color = use_color

    COLOR_MAP = {
        "black": "black",
        "bright_black": "bright_black",
        "red": "red",
        "bright_red": "bright_red",
        "blue": "blue",
        "bright_blue": "bright_blue",
        "green": "green",
        "bright_green": "bright_green",
        "yellow": "yellow",
        "magenta": "magenta",
        "bright_magenta": "bright_magenta",
        "cyan": "cyan",
        "bright_cyan": "bright_cyan",
        "white": "white",
        "bright_white": "bright_white",
        "bold": "bold",
    }

    def colorize(self, text, color_name):
        if not self.use_color or not color_name:
            return text
        rich_color = self.COLOR_MAP.get(color_name)
        if not rich_color:
            return text
        return f"[{rich_color}]{text}[/{rich_color}]"
