# Electional Workflows

Electional astrology, also known as inceptional astrology, is the practice of selecting optimal times and dates to begin or *incept* something. It's arguably one of the oldest and most accessible disciplines: farmers choose (elect) the full moon nearest to the autumnal equinox to  harvest their fall crops, for example.

To elect a time with`ephem`, you will want to use the `ephem cal` and `ephem cast` commands. For something on the same day or near it, `ephem now` has its place here, too. Calling `ephem cal` is no different from referring to *The American Ephemeris* or [PDF versions of the Swiss Ephemeris](https://www.astro.com/swisseph/swepha_e.htm); you're just using the *actual* software library from which those PDFs were generated, and interacting with the information more quickly and easily.

## High-stakes example: Planning a wedding with `ephem cal` and `ephem cast`
Pretend you've been hired to elect a fall wedding that will take place outdoors in northern California, ideally in 2026. The climate means November is a serious possibility. The couple would prefer a weekend but clearly put enough stock in event astrology to ask you, so a weekday wedding is not out of the question.

`ephem cal` takes a year followed by a month written either in full, as a 3-letter abbreviation, or as an integer (1-12), case insensitive:

```sh
$ ephem cal 2026 Sep
$ ephem cal 2026 september
$ ephem cal 2026 9
```

In September 2026, Venus (planet of love [~~was destroyed by global warming~~](https://www.youtube.com/watch?v=qooWnw5rEcI)) ingresses from Libra (its domicile) into Scorpio (its detriment) on Sept. 11. Running `ephem cal 2026 10` shows that it will actually turn retrograde on Oct. 4, re-entering Libra on Oct. 26 before stationing direct on Nov. 15. It's up to you whether Venus' condition by sign matters to you more than its direction.

For the sake of this example, let's say you're looking at November 15-17 for the very end of warm daytime weather and to catch the Moon in Aquarius trining Venus in Libra. Venus is late enough in Libra that it doesn't oppose Saturn in Aries... but you run the risk of Jupiter opposing the Moon and forming a T-square with the Sun since they're all in fixed signs. Oh no. You can probably go back to early September or jump all the way to December to avoid the Sun-Jupiter square of late Scorpio season, but then it wouldn't be a good outdoor wedding, would it? So we've narrowed it down to Sept. 5 for a different air Moon-Venus trine, and added Mars fallen in Cancer to minimize conflict. Here you can just run

```sh
$ ephem cast 2026-09-05 15:00 "Wedding" -z America/Los_Angeles -y 37 -x -122
```

with various times until you get a pleasant ascendant and the malefics off the angles, of course keeping it reasonable. Outdoor weddings want daylight, generally speaking, especially with temperature differences, and I landed around 10-10:30 a.m. for Libra rising or 2-3:30 p.m. for Sagittarius rising. Realistically, this is just one date of several you would find.

## Low-stakes example: Sending an email with `ephem now` and `ephem cast`
This is the much more boring way I use electional astrology and the reason for the `-s/--shift` optional argument specific to `ephem now`.

Scenario: It's 11:45 p.m., and I've just drafted an email I mean to send the next day. If I run
```sh
$ ephem now -s 12h
```

I see that around noon tomorrow, the local ascendant will be Scorpio, which would put a very pleasant Virgo Mercury in the 12th house and make a detrimented Mars in Libra the ruler of this election—terrible! And a waste of a good Mercury transit!  Since it's Virgo season, I know Mercury is near the sun, so sunrise will put Mercury in the first house. I confirm this with

```sh
$ ephem now -s 6h
```

and fine tune it with minutes. I've switched to `ephem cast` because `--shift` only takes weeks, days, hours, and minutes—and land on

```sh
$ ephem cast 2025-09-16 7:32 "email" -z America/New_York
email (Tropical)
2025-09-16 07:32:00 EDT | 2025-09-16 11:32:00 UTC
☉   23 Virgo 51 40
☽   20 Cancer 01 46
☿   26 Virgo 29 58
♀   26 Leo 17 01
♂   26 Libra 05 19
♃   20 Cancer 27 25
♄   28 Pisces 52 42 r
♅    1 Gemini 25 10 r
♆    0 Aries 57 09 r
♇    1 Aquarius 32 31 r
T☊  18 Pisces 20 00
AC  26 Virgo 42 11
MC  26 Gemini 35 55
```
