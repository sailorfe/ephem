# Getting Started

## Your first `ephem` chart

The fastest way to try `ephem` is by running

```sh
$ ephem now
```

The output should look like

```sh
No valid location provided or found in config. No angles will be printed.
Chart of the Moment hyp. (Tropical)
2025-09-15 22:05 UTC

☉   23 Virgo 18 54
☽   12 Cancer 24 27
☿   25 Virgo 28 38
♀   25 Leo 36 06
♂   25 Libra 42 58
♃   20 Cancer 22 15
♄   28 Pisces 55 17 r
♅    1 Gemini 25 27 r
♆    0 Aries 58 04 r
♇    1 Aquarius 32 56 r
T☊  18 Pisces 19 53
```

This purposely mimics Astrodienst's [Chart of the Moment](https://www.astro.com/cgi/chart.cgi?lang=e&act=chm&sdat=&ishkch=1), which prints a chart without geographical information—no angles, no houses. This is plenty useful on its own if you know your own birth chart by heart or use techniques like essential dignity, but the ascendant and midheaven are the two most rapidly changing and geocentric (well, geo-dependent) points of any horoscope.

## Setting location defaults
`ephem` uses decimal degrees for coordinates, which you can find with the following:

1. Look up your locale on Wikipedia.
2. At the top right of the desktop site, you should see hyperlinked coordinates, most likely printed in degrees-minutes-seconds (DMS) like `36°15′0″S 142°25′0″E`. Click this link to go to GeoHack.
3. From GeoHack, note these coordinates in decimal degrees. In our example, this looks like `-36.25, 142.416667`.
4. Rerun the `now` command with these additions:

```sh
# example: Warracknabeal, Australia
ephem now -y -36.25 -x 142.416667 --save-config
```

- Because this example is in the southern hemisphere, `-y/--lat` is negative.
- Because this example is east of the prime meridian, `-x/--lng` is positive.
- `--save-config` is an optional argument that can be run repeatedly to update your locale, display, and calculation preferences. You can read more about configuration under [Display & Configuration Options](./70-display-config.md)

Running this command with `--save-config`  should give you something like
```sh
Saved location settings to /home/user/.config/ephem/ephem.toml
Chart of the Moment (Tropical)
2025-09-15 22:05 UTC @ -36.25 142.416667

☉   23 Virgo 18 55
☽   12 Cancer 24 42
☿   25 Virgo 28 40
♀   25 Leo 36 07
♂   25 Libra 42 59
♃   20 Cancer 22 15
♄   28 Pisces 55 17 r
♅    1 Gemini 25 27 r
♆    0 Aries 58 04 r
♇    1 Aquarius 32 56 r
T☊  18 Pisces 19 53
AC  29 Libra 30 45
MC  17 Cancer 33 04
```

See! Now we have the ascendant and midheaven, `AC` and `MC`.

You can check your current configuration by running `ephem --show-config`. At this point, it should output

```toml
Location defaults:
  Latitude: -36.25
  Longitude: 142.416667
```

If you want to save this moment—your first `ephem` chart!—for the fun of it, run `ephem now --save`. But your first saved chart should probably be *your* birth chart, no?
