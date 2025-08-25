# Changelog

# v1

### 1.0.1 2025-08-25

#### Fixed

- Replaced `sqlite3.OperationError` with helpful message.

## v0

### 0.6.0 2025-08-22

#### Added

- `unittests`

### 0.5.0 2025-08-17

#### Added

- SQLite database and `data` command to interact with it.


### 0.4.0 2025-08-13

#### Added

- Support for sidereal zodiac via global `--offset` option.
- `--list-offsets` global option that prints `index:key` pairs.


### 0.3.0 2025-08-11

#### Added

- Support for local time zone input using `zoneinfo`.


### 0.2.0 2025-08-11

#### Added

- `config` command to replace `--save-config`.

#### Fixed

- `--bare` flag UnboundLocalError


### 0.1.0 2025-08-11

#### Added

- Initial public release.
- Commands: `now`, `cast` and `asc`:
    * `now`, its option `--shift`, and `asc` are designed with electional astrology in mind.
    * `cast` calculates charts for given date, time, and coordinates.
- Detailed help messages and error handling.
- Sensible fallbacks for hypothetical charts, e.g. those missing time and/or place.
