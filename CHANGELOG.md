# Changelog

## 0.1.0 2025-08-11

### Added

- Initial public release.
- Commands: `now`, `cast` and `asc`:
    * `now`, its option `--shift`, and `asc` are designed with electional astrology in mind.
    * `cast` calculates charts for given date, time, and coordinates.
- Detailed help messages and error handling.
- Sensible fallbacks for hypothetical charts, e.g. those missing time and/or place.


## 0.2.0 2025-08-11

### Added

- `config` command to replace `--save-config`.

### Fixed

- `--bare` flag UnboundLocalError


## 0.3.0 2025-08-11

### Added

- Support for local time zone input using `zoneinfo`.
