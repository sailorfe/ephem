# Getting Started

## Your first `ephem` chart

The fastest way to try `ephem` is by running

```sh
$ ephem now
```

The output should look like

```
No valid location provided or found in config. No angles will be printed.
 Chart of the Moment hyp. (Tropical)
 2026-02-06 21:28:02 UTC

  ☉  18 Aquarius 06 02
  ☽  18 Libra 52 58
  ☿  29 Aquarius 54 08
  ♀  25 Aquarius 34 11
  ♂  11 Aquarius 20 49
  ♃  16 Cancer 44 28 r
  ♄  29 Pisces 14 16
  ♅  27 Taurus 27 47
  ♆   0 Aries 18 33
  ♇   3 Aquarius 52 57
 T☊   9 Pisces 05 47
```

This purposely mimics Astrodienst's [Chart of the Moment](https://www.astro.com/cgi/chart.cgi?lang=e&act=chm&sdat=&ishkch=1), which prints a chart without geographical information—no angles, no houses. This is plenty useful on its own if you know your own birth chart by heart or use techniques like essential dignity, but the ascendant and midheaven are the two most rapidly changing and geocentric points of any horoscope.

## Setting location defaults
`ephem` uses decimal degrees for coordinates, which you can find with the following:

1. Look up your locale on Wikipedia.
2. At the top right of the desktop site, you should see hyperlinked coordinates, most likely printed in degrees-minutes-seconds (DMS) like `36°15′0″S 142°25′0″E`. Click this link to go to GeoHack.
3. From GeoHack, note these coordinates in decimal degrees. In our example, this looks like `-36.25, 142.416667`.
4. Rerun the `now` command with these additions:

```sh
# example: Warracknabeal, Australia
$ ephem now -y -36.25 -x 142.416667 --save-config
```

- Because this example is in the southern hemisphere, `-y/--lat` is negative.
- Because this example is east of the prime meridian, `-x/--lng` is positive.
- `--save-config` is an optional argument that can be run repeatedly to update your locale, display, and calculation preferences. You can read more about configuration under [Display & Configuration Options](./70-display-config.md)

Running this command with `--save-config`  should give you something like

```
 Saved location settings to /home/user/.config/ephem/ephem.toml
 Chart of the Moment (Tropical)
 2026-02-06 21:30:33 UTC @ 36.25 142.416667

  ☉  18 Aquarius 06 09
  ☽  18 Libra 54 16
  ☿  29 Aquarius 54 19
  ♀  25 Aquarius 34 19
  ♂  11 Aquarius 20 54
  ♃  16 Cancer 44 27 r
  ♄  29 Pisces 14 16
  🝴  18 Aquarius 06 09
  ♅  27 Taurus 27 47
  ♆   0 Aries 18 33
  ♇   3 Aquarius 52 57
 T☊   9 Pisces 05 47
 AC  17 Aquarius 57 25
 MC   4 Sagittarius 04 44
```

Now we have the ascendant and midheaven, `AC` and `MC`, and the Part of Fortune `🝴`, which is calculated using the ascendant.

You can check your current configuration by running `ephem --show-config`. At this point, it should output

```toml
Location defaults:
  Latitude: -36.25
  Longitude: 142.416667
```

If you want to save this moment—your first `ephem` chart!—for the fun of it, run `ephem now --save`. But your first saved chart should probably be *your* birth chart, no?
