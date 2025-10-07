def validate_year(year):
    """Validate year is within Swiss Ephemeris range (13000 BCE to 3999 CE)."""
    if not (-13000 <= year <= 3999):
        raise ValueError(f"Year must be between 13000 BCE and 3999 CE, got {year}")
    return year
