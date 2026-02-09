class Sign:
    def __init__(self, name, trunc, glyph, trip, quad):
        self.name = name
        self.trunc = trunc
        self.glyph = glyph
        self.trip = trip
        self.quad = quad


class CelestialObject:
    def __init__(self, key, name, glyph):
        self.key = key
        self.name = name
        self.glyph = glyph


class Position:
    def __init__(self, obj, sign, deg, mnt, sec, rx=False):
        self.obj = obj
        self.sign = sign
        self.deg = deg
        self.mnt = mnt
        self.sec = sec
        self.rx = rx

    @property
    def full(self):
        rx_marker = ' r' if self.rx else ''
        return f"{self.deg:>2} {self.sign.name} {self.mnt:02d} {self.sec:02d}{rx_marker}"

    @property
    def short(self):
        rx_marker = ' r' if self.rx else ''
        return f"{self.deg:>2} {self.sign.trunc} {self.mnt:02d} {self.sec:02d}{rx_marker}"

    @property
    def glyph(self):
        rx_marker = ' r' if self.rx else ''
        return f"{self.deg:>2} {self.sign.glyph} {self.mnt:02d} {self.sec:02d}{rx_marker}"
