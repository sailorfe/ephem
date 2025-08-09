SIGNS = {
        "Aries": {
            "trunc": "Ari",
            "glyph": "♈︎",
            "trip": "fire",
            "quad": "cardinal"
            },
        "Taurus": {
            "trunc": "Tau",
            "glyph": "♉︎",
            "trip": "earth",
            "quad": "fixed"
            },
        "Gemini": {
            "trunc": "Gem",
            "glyph": "♊︎",
            "trip": "air",
            "quad": "mutable"
            },
        "Cancer": {
            "trunc": "Can",
            "glyph": "♋︎",
            "trip": "water",
            "quad": "cardinal"
            },
        "Leo": {
            "trunc": "Leo",
            "glyph": "♌︎",
            "trip": "fire",
            "quad": "fixed"
            },
        "Virgo": {
            "trunc": "Vir",
            "glyph": "♍︎",
            "trip": "earth",
            "quad": "mutable"
            },
        "Libra": {
            "trunc": "Lib",
            "glyph": "♎︎",
            "trip": "air",
            "quad": "cardinal"
            },
        "Scorpio": {
            "trunc": "Sco",
            "glyph": "♏︎",
            "trip": "water",
            "quad": "fixed"
            },
        "Sagittarius": {
            "trunc": "Sag",
            "glyph": "♐︎",
            "trip": "fire",
            "quad": "mutable"
            },
        "Capricorn": {
            "trunc": "Cap",
            "glyph": "♑︎",
            "trip": "earth",
            "quad": "cardinal"
            },
        "Aquarius": {
            "trunc": "Aqu",
            "glyph": "♒︎",
            "trip": "air",
            "quad": "fixed"
            },
        "Pisces": {
            "trunc": "Pis",
            "glyph": "♓︎",
            "trip": "water",
            "quad": "mutable"
            }
        }


OBJECTS = {
        "ae": {
            "name": "Sun",
            "glyph": "☉"
            },
        "ag": {
            "name": "Moon",
            "glyph": "☽"
            },
        "hg": {
            "name": "Mercury",
            "glyph": "☿"
            },
        "cu": {
            "name": "Venus",
            "glyph": "♀"
            },
        "fe": {
            "name": "Mars",
            "glyph": "♂",
            },
        "sn": {
            "name": "Jupiter",
            "glyph": "♃"
            },
        "pb": {
            "name": "Saturn",
            "glyph": "♄"
            },
        "ura": {
            "name": "Uranus",
            "glyph": "♅"
            },
        "nep": {
            "name": "Neptune",
            "glyph": "♆"
            },
        "plu": {
            "name": "Pluto",
            "glyph": "♇"
            },
        "mean_node": {
            "name": "Mean Node",
            "glyph": "M☊"
            },
        "true_node": {
            "name": "True Node",
            "glyph": "T☊"
            },
        "asc": {
            "name": "Ascendant",
            "glyph": "AC"
            },
        "mc": {
            "name": "Midheaven",
            "glyph": "MC"
            }
        }

class Colors:
    def __init__(self, use_color=True):
        self.use_color = use_color
        self.codes = {
                "bold": "\033[1m",
                "red": "\033[31m",
                "green": "\033[32m",
                "yellow": "\033[33m",
                "blue": "\033[34m",
                "magenta": "\033[35m",
                "cyan": "\033[36m",
                "bright_red": "\033[91m",
                "bright_green": "\033[92m",
                "bright_blue": "\033[94m",
                "clear": "\033[0m"
            }

    def colorize(self, text, color):
        if self.use_color and color in self.codes:
            return f"{self.codes[color]}{text}{self.codes['clear']}"
        return text
