<div align="center">

# ephem

a minimal, opinionated astrology CLI

[![pypi](https://img.shields.io/pypi/v/ephem-cli.svg)](https://pypi.org/project/ephem-cli/) [![license: agpl v3](https://img.shields.io/badge/license-agpl--3-blue.svg)](./LICENSE)

</div>


**ephem** is a linux-native cli for astrologers, built with hellenistic tradition and electional and horary practice in mind. it generates horoscopes and monthly ephemerides with professional accuracy.

features include:
- all 47 sidereal offsets from [Swiss Ephemeris](https://www.astro.com/swisseph/swephprg.htm)
- the sun, moon, and eight planets (mercury–pluto)
- choice of lunar node calculation method
- clear table output for charts and ephemerides
- graceful handling of incomplete data

deliberately out of scope:
- house cusps and placements
- asteroids
- graphical charts

### table of contents

- [installation](#installation)
- [quick start](#quick-start)
- [usage](#usage)
- [yaml database](#yaml-database)
- [contributing](#contributing)
- [acknowledgments](#acknowledgments)
- [license](#license)

<a name="installation"></a>
## installation

### stable

the stable release of **ephem** can be installed directly from pypi:

```sh
pip install --user ephem-cli    # if you use pip
pipx install ephem-cli          # if you use pipx, especially debian/ubuntu
```

or you can build it from source from the `main` branch:

```sh
git clone https://codeberg.org/sailorfe/ephem.git
cd ephem
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### testing

you can install the current pre-release from codeberg packages:

```sh
# with pip
pip install ephem-cli \
  --pip-args="--index-url https://codeberg.org/api/packages/sailorfe/pypi/simple/ --extra-index-url https://pypi.org/simple --pre"
```

```sh
# with pipx
pip install ephem-cli \
  --pip-args="--index-url https://codeberg.org/api/packages/sailorfe/pypi/simple/ --extra-index-url https://pypi.org/simple --pre"
```

<a name="quick-start"></a>
## quick start

get a chart for right now:
```sh
ephem now
```

save your location to avoid typing coordinates every time:
```sh
ephem now -y 30 -x -80 --save-config
```

cast a chart for a specific date and time:
```sh
ephem cast 1996-08-26 17:20 "Jeon Soyeon" -z Asia/Seoul -y 37.488167 -x 127.085472
```

get a monthly ephemeris:
```sh
ephem cal 1989 dec
```

<a name="usage"></a>
## usage

```sh
ephem {now,cast,cal,data}
```

- `now` and `cast` to calculate and optionally save charts
- `cal` to calculate monthly ephemerides
- `data` to interact with chart database

### calculation commands

```sh
ephem {now,cast} [options]
```

- `--offset` – select sidereal offset from index 0-46 (--list-offsets)
- `-y/--lat` – latitude
- `-x/--lng` – longitude
- `--save` – save to database

**display options**

- `--node {true,mean}` – choose lunar node method
- `--ascii` – use ascii text instead of unicode glyphs, e.g `Sun 5 Pis 58 07` instead of `☉ 5 Pisces 58 07`
- `--theme {sect,mode,element}` – thoughtful color schemes using `LS_COLOR`:
    * `sect` prints diurnal planets in red and nocturnal planets in blue; calculates mercury's sect relative to sun
    * `element` prints fire placements in red, earth placements in green, air placements in gray, and water placements in blue
    * `mode` prints cardinal placements in magenta, fixed placements in yellow, and mutable placements in cyan
- `-c/--classical` – excludes uranus through pluto
- `--no-angles` – skips printing asc or mc
- `--no-geo` – hides coordinates for privacy
- `--no-color` – prints chart in plain text

#### `ephem now`

```sh
ephem now [options]
```

- `-s/--shift` – shift current time forwards or backwards; useful for electional and horary

```sh
# to save default location
$ ephem now -y 30 -x -80 --save-config
```

```sh
# save moment chart to database
$ ephem now --save
```

```sh
$ ephem now -s 2h       # forward 2 hours
$ ephem now -s -30m     # backward 30 minutes
```

#### `ephem cast`

```sh
ephem cast <date> [options]
```

- `-z/--timezone` – IANA tz name string, e.g. `America/New York`, `Asia/Manila`

```sh
# complete data
$ ephem cast 1996-08-26 17:20 "Jeon Soyeon" -z Asia/Seoul -y 37.488167 -x 127.085472
```

```sh
# no time
$ ephem cast 1845-05-19 "Franklin Expedition" -y 51.4504 -x 0.2823
```

```sh
# no location
$ ephem cast 1993-08-16 13:05 "Debian Linux"
```

```sh
# date only
$ ephem cast 1989-12-13 "Taylor Swift"
```

### `ephem cal`

```sh
ephem cal <year> <month> [options]
```

- defaults to current month if passed no arguments
- month can be written as an integer, three-character abbreviation, or in full: `9`/`Sep`/`September`
- options:
    * `--offset` – select ayanamsa; defaults to none (tropical zodiac)
    * `--ascii` – use ascii text instead of unicode glyphs for planets and signs: `16 ♍︎  34 56 ` -> `16 Vir 34 56`

### `ephem data`

```sh
ephem data {view,load,delete}
```
- `data view` – list charts in database by sql id
- `data load N` – run `ephem cast` with saved information
- `data delete N` — delete chart by id
- `data sync` — sync database with YAML charts in `charts/` (see [yaml database](#yaml-database))

#### example workflow

```sh
# get chart sql id
$ ephem data view
[1] Jean Cremers
   UTC:     1957-03-14T18:55:00+00:00
   Local:   1957-03-14T19:55:00+01:00
   Lat:     52.0, Lng: 6.0

[2] Walter Pullen
   UTC:     1971-11-19T19:01:00+00:00
   Local:   1971-11-19T11:01:00-08:00
   Lat:     47.6, Lng: -122.33

[3] Kevin DeCapite
   UTC:     1976-11-29T17:32:00+00:00
   Local:   1976-11-29T12:32:00-05:00
   Lat:     41.3919, Lng: -81.7286

# load saved chart
$ ephem data load 2
 Walter Pullen (Tropical)
 1971-11-19 19:01 UTC @ 47.6 -122.33

 ☉  26 Scorpio 47 30
 ☽  16 Sagittarius 09 58
 ☿  18 Sagittarius 15 15
 {etc...}

# delete chart by id
$ ephem data delete 3
✅ deleted chart 3
```

<a name="yaml-database"></a>
## yaml database

**ephem** is designed to be perfectly usable with only `data {view,load,delete}`, but power users can create, edit, and sync charts by working directly with YAML files.

### structure

the xdg-compliant directory structure is:

```
.local/share/ephem
    |- charts/
    |   |- client-amy.yaml
    |   |- famous-nick-cave.yaml
    |   |- event-franklin-expedition.yaml
    |   `- {etc...}
    `- ephem.db
```

### sync behavior

`ephem data sync` is bi-directional:
- reads `ephem.db` to find charts added via `ephem {now,cast} --save` that don't have corresponding YAML files
- reads `charts/` to find YAML files that aren't yet in `ephem.db`

### deletion behavior

to completely delete a chart, you need to do both:
1. `ephem data delete <id>` 
2. manually delete the YAML file 

this prevents `ephem data sync` from re-adding deleted charts. the extra step also serves as backup protection against accidental deletions. if you never use `ephem data sync`, you can ignore the YAML files entirely.

### file format

the YAML files contain time and geographic data with expandable `_metadata`:

```yaml
name: Nick Cave
timestamp_utc: '1957-09-22T02:20:00+00:00'
timestamp_input: '1957-09-22T12:20:00+10:00'
latitude: -36.25
longitude: 142.416667
_metadata:
  created: '2025-09-10T12:55:37.004823'
  source: ephem_cli
  tags: [famous, musician, adb, rodden-c]
```

<a name="conributing"></a>
## contributing

**ephem** is in early development. contributions are welcome, especially from developers with experience in astrology software, but what it *really* needs at this stage is testers. let me know if that's you and i'll start a discord: [hello@sailorfe.dev](mailto:hello@sailorfe.dev).

<a name="acknowledgments"></a>
## acknowledgments

**ephem** draws inspiration from:

- [Swiss Ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm) and [Astro.com](https://www.astro.com/horoscope)
- [Astrolog](https://astrolog.org/astrolog.html) by Walter Pullen
- [Planetdance](http://www.jcremers.com/Home.html) by Jean Cremers
- *The American Ephemeris* by Neil F. Michelsen and Rique Pottenger
- *Astrological Chart Calculations* by Bruce Scofield

<a name="license"></a>
## license

licensed under AGPL v3 per the Swiss Ephemeris; see [LICENSE](./LICENSE) file for details.