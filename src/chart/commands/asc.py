import swisseph as swe
from chart.constants import SHORT
from chart.utils import get_locale
from datetime import datetime, timezone

def run(args):
    lat, lng, approx_locale, *_ = get_locale(args)

    now = datetime.now(timezone.utc)

    jd = swe.julday(
        now.year,
        now.month,
        now.day,
        now.hour + now.minute / 60 + now.second / 3600
    )

    houses = swe.houses(jd, lat, lng, b'W')
    asc_deg = houses[1][0]
    dms = swe.split_deg(asc_deg, 8)
    sign = SHORT[dms[4]]

    if approx_locale is True:
        print(f"No location given or found in config; using Null Island (0,0).")
    print(f"AC {dms[0]} {sign} {dms[1]}")

