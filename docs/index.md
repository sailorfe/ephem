# Introduction

> Astrology is alive. It is whole, functional and independent.
> It has been present in the human spirit from the first civilizations
> when Man began his long search for meaning.
> It has spanned eras and cultures,
> yet always remains perfectly current and relevant.
> It is clear, clean, and objective knowledge: containing nothing nebulous.
> Just as it must be clear for one to view the stars at night,
> so too thought must be clear for one to master astrological interpretation.[^1]

Everything has a horoscope, and computing makes it exceptionally easy to keep track of dates and times. Where western astrology has been dominated by natal astrology—something static against which to judge the dynamic—Ephem's focus is on the ephemeral. It's easiest to run `ephem now` for a snapshot of the *second* you send the command.

For example, this application's first Git commit can be considered its birth or inception:

```
commit 7587dc9634fd682a5a1b40da0f4e54498d34adde
Author: sailorfe <sailorfe@proton.me>
Date:   Wed Aug 6 13:57:13 2025 -0400
    initial
```

Its chart generated with *itself* (whew) is

```
 ephem (Tropical)
 2025-08-06 17:57:13 UTC @ 27.45 -82.3775

  ☉  14 Leo 31 29        
  ☽  13 Capricorn 04 49  
  ☿   5 Leo 21 05 r      
  ♀   7 Cancer 38 44     
  ♂  29 Virgo 51 32      
  ♃  12 Cancer 55 45     
  ♄   1 Aries 26 07 r    
  🝴  14 Aries 33 00      
  ♅   1 Gemini 04 37     
  ♆   1 Aries 53 44 r    
  ♇   2 Aquarius 17 54 r 
 T☊  18 Pisces 46 07 r   
 AC  15 Scorpio 59 40    
 MC  20 Leo 02 35
```


This tutorial assumes astrological literacy but not necessarily command-line experience. Some resources I recommend:

- [Learn enough command line to be dangerous](https://www.learnenough.com/command-line-tutorial/basics)
- [Introduction to the command line](https://tutorials.codebar.io/command-line/introduction/tutorial.html)

By the end, you will have set your default location, saved your own birth chart, elected an event, and answered a horary question, all in the terminal.

[^1]: Helena Avelar and Luis Ribeiro, *On the Heavenly Spheres*, 2010.
