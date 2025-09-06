# ephem

**ephem** is a minimal, opinionated astrology CLI.

it provides offline, terminal-based horoscope calculations using the [swiss ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm), serving as a portable alternative to web-based chart generators.

## features
- configurable default location
- sidereal ayanamsa support
- readable, terminal-friendly table output
- handles incomplete data gracefully

## installation

you can install **ephem-cli** directly from [PyPI](https://pypi.org/project/ephem-cli).


```sh
pip install --user ephem-cli    # if you use pip
pipx install ephem-cli          # if you use pipx
```

or you can grab a pre-release from the codeberg [packages](https://codeberg.org/sailorfe/ephem/packages) tab.


### from source

```sh
git clone https://codeberg.org/sailorfe/ephem.git
cd ephem
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## usage

```sh
# chart for the current moment
ephem now

# chart for a specific date and time; location optional
ephem cast 1993-08-16 13:05 "Debian Linux"

# ephemeris for specific month
ephem cal 1989 Dec
```

## commands

| command   | description                           |
| ----------| ------------------------------------- |
| `now`     | calculate the chart of the moment     |
| `cast`    | calculate chart for an event or birth |
| `cal`     | calculate monthly ephemeris table     |
| `data`    | manage chart database                 |

## roadmap
### v2

- [x] replace configparser with tomllib
- [x] calendar view for current and specified months
- [ ] YAML-based database interaction

## contributing

ephem is in early development. contributions are welcome, especially from developers with experience in astrology software.

## acknowledgments

ephem draws inspiration from:

- [swiss ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm) and [Astro.com](https://www.astro.com/horoscope)
- [astrolog](https://astrolog.org/astrolog.html) by walter pullen
- [planetdance](http://www.jcremers.com/Home.html) by jean cremers
- *the american ephemeris* by neil f. michelsen and rique pottenger
- *astrological chart calculations* by bruce scofield

## more information

- [changelog](./CHANGELOG.md) – version history and updates.
- [cevlogs](https://sailorfe.codeberg.page) — real-time development notes
- [hackstrology](https://buttondown.com/hackstrology) — biweekly astrology newsletter

## license

licensed under AGPL v3; see [LICENSE](./LICENSE) file for details.
