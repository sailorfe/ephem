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

    COLOR_MAP = {
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
        "bold": "bold",
    }

    def colorize(self, text, color_name):
        if not self.use_color or not color_name:
            return text
        rich_color = self.COLOR_MAP.get(color_name)
        if not rich_color:
            return text
        # Wrap text in Rich markup tags
        return f"[{rich_color}]{text}[/{rich_color}]"

