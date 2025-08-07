SIGNS = ["Aries", "Taurus", "Gemini", "Cancer",
         "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


SHORT = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir",
         "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]


GLYPHS = {
        "ae": "☉",
        "ag": "☽",
        "hg": "☿",
        "cu": "♀",
        "fe": "♂",
        "sn": "♃",
        "pb": "♄",
        "ura": "♅",
        "nep": "♆",
        "plu": "♇",
        "mean_node": "M☊",
        "true_node": "T☊",
        "asc": "AC",
        "mc": "MC"
        }


VERBOSE = {
        "ae": "Sun",
        "ag": "Moon",
        "hg": "Mercury",
        "cu": "Venus",
        "fe": "Mars",
        "sn": "Jupiter",
        "pb": "Saturn",
        "ura": "Uranus",
        "nep": "Neptune",
        "plu": "Pluto",
        "mean_node": "Mean Node",
        "true_node": "True Node",
        "asc": "Ascendant",
        "mc": "Midheaven"
        }


class Colors:
    def __init__(self, use_color=True):
        self.use_color = use_color
        self.codes = {
                "bold": "\033[1m",
                "bright_red": "\033[91m",
                "bright_blue": "\033[94m",
                "red": "\033[31m",
                "blue": "\033[34m",
                "clear": "\033[0m"
            }

    def colorize(self, text, color):
        if self.use_color and color in self.codes:
            return f"{self.codes[color]}{text}{self.codes['clear']}"
        return text
