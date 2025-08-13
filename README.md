# 🌠 Ephem

**Ephem** is a minimal, opinionated, and configurable horoscope CLI designed with electional astrology and premodern revivalism in mind. It aims to be a portable, terminal version of print ephemerides, proving a reliable offline alternative to web-based chart generators.

## 📜 Features
- [SwissEphemeris](https://www.astro.com/swisseph/swephinfo_e.htm) calculations
- Clear, readable table output 📊
- Multiple display and formatting modes
- Configurable default place and formatting ⚙️
- Accommodates incomplete data with sensible placeholders
- Default ANSI color scheme follows Hellenistic sect

## 💻 Installation

```sh
pip install ephem-cli
```

## 🌙 Usage

```shell
ephem now
ephem cast 1993-08-16 13:05 "Debian Linux"
```

### Commands
| Command  | Description                        |
| -------- | ---------------------------------- |
| `now`    | Calculate chart of the moment 🌌   |
| `cast`   | Calculate chart for event/birth 🎂 |
| `asc`    | Print current local ascendant 🌅   |
| `config` | Update saved preferences ⚙️        |

## 🪐 Roadmap

### 1.0.0
- [ ] Save, list, and view chart data from a SQLite database
- [x] Sidereal zodiac and custom offset support
- [x] Conversion from local time to UTC and vice versa
- [x] Alternate ANSI color schemes by sign triplicity or quadruplicity
- [x] Integrate shell scriptable clock from [ascendant](https://codeberg.org/sailorfe/ascendant)
- [x] `config.ini` with configparser
- [x] Option to hide coordinates from printing

### Future

- [ ] HTTP database API
- [ ] SVG wheel and square charts; will require different house systems finally


```
	                   ,dPYb,                                
                      IP'`Yb                                
                      I8  8I                                
                      I8  8'                                
  ,ggg,   gg,gggg,    I8 dPgg,    ,ggg,    ,ggg,,ggg,,ggg,  
 i8" "8i  I8P"  "Yb   I8dP" "8I  i8" "8i  ,8" "8P" "8P" "8, 
 I8, ,8I  I8'    ,8i  I8P    I8  I8, ,8I  I8   8I   8I   8I 
 `YbadP' ,I8 _  ,d8' ,d8     I8, `YbadP' ,dP   8I   8I   Yb,
888P"Y888PI8 YY88888P88P     `Y8888P"Y8888P'   8I   8I   `Y8
          I8                                                
          I8                                                
          I8                                                
          I8                                                
```

## ✨ Contributing

This is my self-taught Python bootcamp project, so very much a work in progress as I learn. I welcome early testers and feedback, but for now I'm keeping active development mostly solo.

Astrology i s a niche subject, so I'm prioritizing input from other astrologers during these early stages. Once v1.0.0 reaches feature completion, I plan to launch a Discord server for community collaboration.

## 🙏🏼 Acknowledgments

This project is strongly influenced by:

- The [Swiss  Ephemeris](https://www.astro.com/swisseph/swephinfo_e.htm) and [Astro.com](https://astro.com), especially its Chart of the Moment ☉☽☿ and Hellenstic chart drawing style (thanks Chris Brennan!)
-  Walter Pullen of [Astrolog](https://astrolog.org/astrolog.htm), still my daily driver for graphical charts that I've used as a CLI from the start
-  Jean Cremers and the [Planetdance](http://www.jcremers.com/Home.html) community, what I used before I switched to Linux
-  *Astrological Chart Calculations* by Bruce Scofield
-  *The American Ephemeris* by Neil F. Michelsen and Rique Pottenger
-  [The Association for Younger Astrologers](https://youngastrologers.org)
- My first mentor, D'Aine Greene, who predicted I would do this six years in advance when I didn't know a single programming language

## 📚 More information

- [Changelog](./CHANGELOG) – Version history with major changes and bug fixes.
- [Devlogs](https://sailorfe.codeberg.page) – More about the tech stack and really basic Python realizations had in real-time.
- [Hackstrology](https://buttondown.com/hackstrology) – A broader, biweekly astrology newsletter with periodic progress updates for non-developers.

## 📃 License
Per the original [Swiss Ephemeris C library](https://www.astro.com/swisseph/swephinfo_e.htm), this software is licensed under the AGPL.
