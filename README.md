# electional

**electional** is an opinionated horoscope CLI designed with electional astrology in mind. by default, it calculates the chart of the moment relative to your geolocated IP coordinates, but also accepts input for specific dates like nativities and other past and future events.

by "opinionated," i mean i wrote it with methodological and traditional biases, not that it offers any sort of interpretation or judgment. the ANSI colors divide the seven visible planets by sect, including mercury; the unicode planetary glyphs lack labels; and the flags for the seven visible planets are their metals in medieval alchemy.

- [usage](#usage)
- [installation](#installation)
- [contributing](#contributing)
- [license](#license)

<a name="usage"></a>
## usage

```sh
$ electional -h
usage: electional [-h] {chart,asc} ...

A horoscope CLI for electional astrology.

positional arguments:
  {chart,asc}  subcommand help
    chart      calculate the chart of the moment or an event/birth chart
    asc        calculate current local ascendant with IP geolocation or given coordinates

options:
  -h, --help   show this help message and exit
```

```sh
$ electional chart -h
usage: electional chart [-h] [-e DATE TIME LAT LNG] [-t TITLE] [-s] [-p] [-c] [-a] [--node {true,mean}] [LAT [LNG ...]]

positional arguments:
  LAT LNG               optional coordinates for chart of the moment

options:
  -h, --help            show this help message and exit
  -e, --event DATE TIME LAT LNG
                        calculate chart for specific date/time/place (YYYY-MM-DD HH:MM y x)
  -t, --title TITLE     e.g. <Your Name>, "Now", "Full Moon"
  -s, --short           print truncated placements, e.g. 21 Sco 2
  -p, --plain           disable ANSI colors
  -c, --classical       exclude Uranus through Pluto
  -a, --approximate     given a date but no time and/or place, use UTC noon and don't print angles
  --node {true,mean}    choose lunar node calculation method
```

```sh
$ electional asc -h
usage: electional asc [-h] [LAT [LNG ...]]

positional arguments:
  LAT LNG     optionally provide coordinates

options:
  -h, --help  show this help message and exit
```

<a name="installation"></a>
## installation

as of writing, this project hasn't been packaged for release because... i don't know how (yet). check back soon or clone this repo for the source!

<a name="contributing"></a>
## contributing

i welcome contributions!! this is my biggest python project so far. please help, please fork.

### ideas

- [ ] conversion from local time to UTC and vice versa
- [ ] alternate ANSI color schemes by sign triplicity or quadruplicity
- [ ] option to print coordinates
- [ ] pseudo "wheel" text output option in the style of Astrolog

<a name="license"></a>
## license

per the original [swiss ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm), this software is licensed under the AGPL.
