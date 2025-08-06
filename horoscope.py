from datetime import datetime
import swisseph as swe
from constants import SIGNS, SHORT

def get_julian_days(date_str, time_str):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd_now = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)
    # one julian minute per https://ssd.jpl.nasa.gov/tools/jdc/#/cd
    jd_then = jd_now - 0.0006944998167455196
    return jd_now, jd_then


def get_planets(jd_now, jd_then):
    planets = []
    for planet in range(12):
        dd_now = swe.calc_ut(jd_now, planet)[0][0]
        dd_then = swe.calc_ut(jd_then, planet)[0][0]
        dms = swe.split_deg(dd_now, 8)
        planets.append({
            'deg': dms[0],
            'sign': SIGNS[dms[4]],
            'short': SHORT[dms[4]],
            'mnt': dms[1],
            'sec': dms[2],
            'rx': dd_then > dd_now,
            'lng': dd_now
            })
    return planets


def get_angles(jd_now, lat, lng):
    angles = []
    asc_mc = swe.houses(jd_now, lat, lng, b'W')[1]
    for angle in asc_mc[:2]:
        dms = swe.split_deg(angle, 8)
        angles.append({
            'deg': dms[0],
            'sign': SIGNS[dms[4]],
            'short': SHORT[dms[4]],
            'mnt': dms[1],
            'sec': dms[2]
            })
    return angles


def build_horoscope(planets, angles):
    keys = [
            "ae",
            "ag",
            "hg",
            "cu",
            "fe",
            "sn",
            "pb",
            "ura",
            "nep",
            "plu",
            "mean_node",
            "true_node"
            ]

    horoscope = {}

    for i in range(len(keys)):
        key = keys[i]
        planet = planets [i]

        deg= planet['deg']
        sign = planet['sign']
        short = planet['short']
        mnt = planet ['mnt']
        sec = planet ['sec']
        rx = planet ['rx']

        formatted = f"{deg} {sign} {mnt} {sec}{' r' if rx else ''}"
        truncated = f"{deg} {short} {mnt}{' r' if rx else ''}"

        horoscope[key] = {
                "full": formatted,
                "short": truncated
                }

    angle_keys = ["asc", "mc"]
    for i, key in enumerate(angle_keys):
        angle = angles[i]
        deg = angle['deg']
        sign = angle['sign']
        short = angle['short']
        mnt = angle['mnt']
        sec = angle['sec']

        formatted = f"{deg} {sign} {mnt} {sec}"
        truncated = f"{deg} {short} {mnt}"

        horoscope[key] = {
                "full": formatted,
                "short": truncated
                }

    return horoscope
