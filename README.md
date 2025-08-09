# chart

**chart** (tentative name) is a minimal, opinionated, and configurable horoscope CLI designed with electional astrology and premodern revivalism in mind.

![made with vhs by charm](./chart-moonqueen.gif)

### features

- **`chart now`** shows the current chart for your location.
- **`chart asc`** prints the ascendant for your location, for an efficient, scriptable clock.
- **`chart cast DATE TIME TITLE`** casts a chart for a specific event, like a birth.
- `--save-config` saves default place and display settings to `chart.ini`
- accommodates hypothetical charts from incomplete information by defaulting to UTC noon or Null Island (0,0).
- default ANSI coloring following hellenistic sect

### table of contents

- [usage](#usage)
- [installation](#installation)
- [roadmap](#roadmap)
- [contributing](#contributing)
- [license](#license)

<a name="usage"></a>
## usage

show chart of the moment for your location:

```sh
chart now
```

cast an event or birth chart:

```sh
chart cast 1998-08-26 8:20 "Jeon Soyeon" --lat 37.49 --lng 127.0855
```

```sh
chart cast 1993-08-16 13:05 "Debian Linux"
```

<a name="installation"></a>
clone this repo:

```sh
git clone https://codeberg.org/sailorfe/chart.git
```

create a venv (optional):

```sh
python -m venv venv
source venv/bin/activate
```

install dependencies:

```sh
pip install -r requirements.txt
```

<a name="roadmap"></a>
## roadmap

- [ ] save a database of `YAML` chart data
- [ ] follow [NO_COLOR](https://no-color.org)
- [ ] alternate ANSI color schemes by sign triplicity or quadruplicity
- [ ] conversion from local time to UTC and vice versa
- [ ] pseudo "wheel" text output option in the style of Astrolog
- [x] integrate shell scriptable clock from [ascendant](https://codeberg.org/sailorfe/ascendant)
- [x] `config.ini` with configparser!
- [x] ~~option to print or hide coordinates~~

<a name="contributing"></a>
## contributing

this project is very new, and i welcome contributions!! this is my biggest python project so far. please help, please fork.

<a name="license"></a>
## license

per the original [swiss ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm), this software is licensed under the AGPL.
