# chart

**chart** is a minimal, opinionated, and configurable horoscope CLI designed with electional astrology and premodern revivalism in mind. `chart now` calculates the chart of the moment relative for your locale, while `chart cast` accepts input for specific dates like nativities and other past and future events.

pair with [ascendant](https://codeberg.org/sailorfe/ascendant) for an efficient scriptable clock 🤓

![made with vhs by charm](./chart-moonqueen.gif)

- [usage](#usage)
- [installation](#installation)
- [contributing](#contributing)
- [license](#license)

<a name="usage"></a>
## usage

```sh
$ chart -h
usage: chart [-h] {now,cast} ...

chart is a minimal, opinionated and configurable horoscope CLI 🪐🌌

positional arguments:
  {now,cast}  subcommand help
    now       calculate the chart of the moment
    cast      calculate an event chart

options:
  -h, --help  show this help message and exit

```

### configuration

you can generate this with either `chart now --save-config` or `chart cast --save-config`:

```ini
[location]
# floats in decimal degrees for precision
lat = 36.0              # N is positive, S is negative
lng = -86.0             # E is positive, W is negative

[display]
classical = False       # set with --classical or -c
brief = False           # set with --brief or -b
verbose = False         # set with --verbose or -v
no-color = False        # set with --no-color or -m
no-angles = False       # set with --no-angles or -z
no-coordinates = False  # set with --no-coordinates or -p
node = true             # not a boolean! this is a string; other option is 'mean'
```

<a name="contributing"></a>
## contributing

this project is very new, and i welcome contributions!! this is my biggest python project so far. please help, please fork.

### roadmap

- [x] `config.ini` with configparser!
- [ ] save a database of `YAML` birth/event info
- [ ] follow [NO_COLOR](https://no-color.org)
- [ ] alternate ANSI color schemes by sign triplicity or quadruplicity
- [ ] conversion from local time to UTC and vice versa
- [ ] pseudo "wheel" text output option in the style of Astrolog
- [x] ~~option to print or hide coordinates~~

<a name="license"></a>
## license

per the original [swiss ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm), this software is licensed under the AGPL.
