# ephem

**ephem** is a minimal, opinionated, and configurable horoscope CLI designed with electional astrology and premodern revivalism in mind. It aims to be a portable, terminal version of print ephemerides in widespread use among astrologers prior to personal computers and GUIs, providing a reliable offline alternative to web-based chart generators.

### Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Installation](#installation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

<a name ="features"></a>
## Features

- `ephem now` shows the current chart for your location.
- `ephem asc` prints the ascendant for your location, for an efficient, scriptable clock.
- `ephem cast DATE TIME TITLE` casts a chart for a specific event, like a birth.
- `--save-config` saves default place and display settings to `ephem.ini`
- Accommodates incomplete information by defaulting to UTC noon or Null Island (0,0) for hypothetical charts.
- Default ANSI coloring following Hellenistic planetary sect along with sign-based element and modality themes.

<a name="usage"></a>
## Usage

Show chart of the moment for your location:

```sh
ephem now
```

Cast an event or birth chart:

```sh
ephem cast 1998-08-26 8:20 "Jeon Soyeon" --lat 37.49 --lng 127.0855
```

```sh
ephem cast 1993-08-16 13:05 "Debian Linux"
```

<a name="installation"></a>
## Installation

### PyPI

```sh
pip install ephem
```

### From source
Clone this repo:

```sh
git clone https://codeberg.org/sailorfe/ephem.git
```

Create a venv:

```sh
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Install locally:

```sh
pip install .
```

<a name="roadmap"></a>
## Roadmap

- [ ] Save, list, and view chart data from a SQLite database
- [ ] Conversion from local time to UTC and vice versa
- [ ] Pseudo "wheel" text output option in the style of Astrolog
- [x] Alternate ANSI color schemes by sign triplicity or quadruplicity
- [x] Integrate shell scriptable clock from [ascendant](https://codeberg.org/sailorfe/ascendant)
- [x] `config.ini` with configparser!
- [x] Option to hide coordinates from printing.

<a name="contributing"></a>
## Contributing

This is my self-taught Python bootcamp project, so very much a work in progress as I learn. I welcome early testers and feedback but plan to keep development mostly solo for now.

<a name="license"></a>
## License

Per the original [Swiss Ephemeris C library](https://www.astro.com/swisseph/swephinfo_e.htm), this software is licensed under the AGPL.
