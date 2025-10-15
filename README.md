<div align="center">

<img src="./assets/vhs.gif">

# ephem

a minimal, opinionated astrology CLI tool

[![pypi](https://img.shields.io/pypi/v/ephem-cli.svg)](https://pypi.org/project/ephem-cli/) [![license: agpl v3](https://img.shields.io/badge/license-agpl--3-blue.svg)](./LICENSE)

</div>


`ephem` is a linux-native cli for astrologers, built on hellenistic tradition with electional and horary practice in mind. it generates horoscopes and monthly ephemerides with professional accuracy, and stores time and geodata in a local database that can be edited as YAML files.

currently supports:
- all 47 sidereal offsets from the [Swiss Ephemeris](https://www.astro.com/swisseph/swephprg.htm)
- the sun, moon, and eight planets (mercury–pluto)
- choice of lunar node calculation method
- clear table output for charts and ephemerides
- graceful handling of incomplete data

deliberately out of scope:
- house cusps and placements
- graphical charts
- asteroids

### table of contents

- [installation](#installation)
- [usage](#usage)
    * [examples](#examples)
    * [tutorial](#tutorial)
- [testing](#testing)
- [contributing](#contributing)
- [acknowledgments](#acknowledgments)
- [license](#license)

<a name="installation"></a>
## installation

### build dependencies

because [pyswisseph](https://github.com/astrorigin/pyswisseph) wraps the Swiss Ephemeris C library, you'll need to run the following:

- **debian-based**: `sudo update && sudo apt install build-essential python3-dev`
- **fedora/rhel**: `sudo dnf install @development-tools python3-devel`
- **arch**: `sudo pacman -Syu base-devel python`
- **alpine**: `doas apk add base python3-dev`
- **macOS**: install **XCode Command Line Tools** (`xcode select --install`)

### stable

the stable release of `ephem` can be installed directly from [pypi](https://pypi.org/project/ephem-cli):

```sh
# run directly without installing
uvx --from ephem-cli ephem

# global installation
uv tool install ephem-cli
# or
pipx install ephem-cli
```

or you can build it from source from the `main` branch:

```sh
git clone https://codeberg.org/sailorfe/ephem.git
cd ephem
uv run -m ephem.cli             # run directly
# or
uv sync && uv run -m ephem.cli     # for development
```

### testing

you can install the current pre-release from codeberg:

```
# run pre-release directly from codeberg
uvx --from https://codeberg.org/sailorfe/ephem ephem-cli

# or install pre-release
uv tool install ephem-cli \
  --index https://codeberg.org/api/packages/sailorfe/pypi/simple/ \
  --prerelease allow
```

<a name="usage"></a>
## usage

```sh
ephem {now,cast,cal,data}
```

- `now` and `cast` to calculate and optionally save charts
- `cal` to calculate monthly ephemerides
- `data` to interact with chart database

<a name="examples"></a>
### examples

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

<a name="tutorial"></a>
### tutorial

for more detailed examples, see [the ephem tutorial](https://sailorfe.codeberg.page/ephem). (i think it's pretty good.)

<a name="testing"></a>
## testing

`ephem` has a test suite. run it with:

```sh
make test
```

these tests currently focus on CLI behavior and database interactions since core calculations are handled by the Swiss Ephemeris library. more tests are planned as the project grows!

<a name="contributing"></a>
## contributing

`ephem` is in early development. contributions are welcome, especially from developers with experience in astrology software, but what it *really* needs at this stage is testers. [join the humble discord server](https://discord.gg/b3vA5ZhSu2)!

<a name="acknowledgments"></a>
## acknowledgments

`ephem` draws inspiration from:

- [Swiss Ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm) and [Astro.com](https://www.astro.com/horoscope)
- [Astrolog](https://astrolog.org/astrolog.html) by Walter Pullen
- [Planetdance](http://www.jcremers.com/Home.html) by Jean Cremers
- *The American Ephemeris* by Neil F. Michelsen and Rique Pottenger
- *Astrological Chart Calculations* by Bruce Scofield

<a name="license"></a>
## license

licensed under AGPL v3 per the Swiss Ephemeris; see [LICENSE](./LICENSE) file for details.
