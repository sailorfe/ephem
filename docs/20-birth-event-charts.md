# Birth and Event Charts

## `ephem cast`

The command structure for `ephem cast` goes:

```sh
$ ephem cast DATE [TIME] [NAME STRING] [options]
```
 
 After you've typed however much time data you have and an optional chart name, every argument—latitude, longitude, and time zone—can follow in any order.  These all result in the same chart:

```sh
# every argument
$ ephem cast 1996-08-26 17:20 "Jeon Soyeon" -z Asia/Seoul -y 37.488167 -x 127.085472

# no title, coordinates before tz, and -x/--lng before -y/--lat
$ ephem cast 1996-08-26 17:20 -x 127.085472 -y 37.488167 -z Asia/Seoul

# you can even throw the time zone in the middle of the coordinates
$ ephem cast 1996-08-26 17:20 -y 37.488167 -z Asia/Seoul -x 127.085472
```

 `ephem cast` is designed to accept incomplete data for approximate  charts. If you only have a date, it will give you *something* to work with. Given only a date, e.g. `ephem cast 1989-12-13 "Taylor Swift"`, it:
 
 - uses UTC noon
 - uses your location defaults if configured; otherwise, Null Island (0,0)
- doesn't print angles
- appends `hyp.` (hypothetical) after the chart title

All you need to do to save a chart to your database (`~/.local/share/ephem/ephem.db`) is append a `--save` flag anywhere in your `cast` command.

```sh
$ ephem cast 1996-08-26 17:20 "Jeon Soyeon" -z Asia/Seoul -y 37.488167 -x 127.085472 --save
```

This prints a confirmation message after the chart output:
```
Jeon Soyeon (Tropical)
1996-08-26 17:20:00 KST | 1996-08-26 08:20:00 UTC @ 37.488167 127.085472

☉    3 Virgo 22 22
☽   29 Capricorn 28 28
☿    0 Libra 05 24
♀   17 Cancer 43 45
♂   20 Cancer 47 56
♃    7 Capricorn 55 39 r
♄    6 Aries 12 36 r
♅    1 Aquarius 24 41 r
♆   25 Capricorn 24 50 r
♇    0 Sagittarius 24 14
T☊   8 Libra 28 00 r
AC  28 Capricorn 09 31
MC  19 Scorpio 24 02

Chart saved at index 1.
```

You can verify it was saved by running `ephem data view`:
```
[1] Jeon Soyeon
   UTC:     1996-08-26T08:20:00+00:00
   Local:   1996-08-26T17:20:00+09:00
   Lat:     37.488167, Lng: 127.085472
```

And recalculate it with `ephem data load 1`.

There is a more detailed breakdown of how to interact with `ephem`'s saved data under [Database Management](./50-database-management.md).

## Time zone support
One of the biggest difference between `ephem now` and `ephem cast` is that `now` uses your computer's system time—printed in UTC by default—while `cast` works with local time.

For casting charts, especially verbatim from client intake, you'll need an IANA time zone string. `ephem` uses the Python standard library module [`zoneinfo`](https://docs.python.org/3/library/zoneinfo.html), which rules because it handles daylight savings for you. You can list all available zone strings alphabetically with `ephem --list-zones`, but this list is nearly 500 items long. There are various online sources where you can look up tz strings instead, but I like [Datetime.app](https://datetime.app/iana-timezones). As a quick, US-centric guide:

- UTC-5: `America/New_York` (Eastern Standard Time)
- UTC-6: `America/Chicago` (Central Standard Time)
- UTC-7: `America/Denver` (Mountain Standard Time)
- UTC-8: `America/Los_Angeles` (Pacific Standard Time)

Alternately, you can convert any time to UTC and avoid `-z/--timezone` altogether, but this gets weird near midnight or the International Date Line, and it's good practice to stay true to the data as given.
