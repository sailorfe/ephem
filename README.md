# Ephem

**Ephem** is a minimal, opinionated astrology CLI.

It provides offline, terminal-based horoscope calculations using the [Swiss Ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm), serving as a portable alternative to web-based chart generators.

## Features
- Swiss Ephemeris calculations
- Readable, terminal-friendly table output
- Configurable default location
- Multiple display modes and ANSI color schemes
- Handles incomplete data gracefully

## Installation

You can install **ephem-cli** directly from [PyPI](https://pypi.org/project/ephem-cli).

### With `pipx`

`pipx` installs Python command-line apps in their own isolated environments, so you don’t have to worry about dependencies messing with your system.

```sh
pipx install ephem-cli
```

### With `pip`

If you don’t have `pipx`, you can install with `pip`:

```sh
pip install --user ephem-cli
```

Make sure your Python user bin directory (often `~/.local/bin`) is on your `$PATH`.

### From source

Clone the repo and install in editable mode:

```sh
git clone https://codeberg.org/sailorfe/ephem.git
cd ephem
pip install -e .
```

## Usage

```sh
# Chart for the current moment
ephem now

# Chart for a specific date and time; location optional
ephem cast 1993-08-16 13:05 "Debian Linux"
```

## Commands

| Command   | Description                           |
| ----------| ------------------------------------- |
| `now`     | Calculate the chart of the moment     |
| `cast`    | Calculate chart for an event or birth |
| `asc`     | Print current local ascendant         |
| `data`    | Manage chart database                 |
| `config`  | Update saved preferences              |

## Roadmap

### v1.0.0
- [x] Write unit tests
- [x] Save, list, and view chart data in an SQLite database
- [x] Sidereal zodiac and custom ayanamsa support
- [x] Convert local time input to UTC
- [x] Alternate ANSI color schemese
- [x] Integrate [ascendant](https://codeberg.org/sailorfe/ascendant)
- [x] `config.ini` with `configparser`
- [x] Option to hide coordinates in output

### Future

- [ ] calendar view for current and specified months
- [ ] YAML-based database interaction
- [ ] fight with configparser and argparse over display settings
- [ ] SVG wheel and square charts with multiple house systems

## Contributing

Ephem is in early development. Contributions are welcome, especially from developers with experience in astrology software.

## Acknowledgments

Ephem draws inspiration from:

- [Swiss Ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm) and [Astro.com](https://www.astro.com/horoscope)
- [Astrolog](https://astrolog.org/astrolog.html) by Walter Pullen
- [Planetdance](http://www.jcremers.com/Home.html) by Jean Cremers
- *The American Ephemeris* by Neil F. Michelsen and Rique Pottenger
- *Astrological Chart Calculations* by Bruce Scofield

## More information

- [Changelog](./CHANGELOG.md) – Version history and updates.
- [Devlogs](https://sailorfe.codeberg.page) — Real-time development notes
- [Hackstrology](https://buttondown.com/hackstrology) — Biweekly astrology newsletter

## License

Licensed under AGPL v3. See [LICENSE](./LICENSE) file for details.
