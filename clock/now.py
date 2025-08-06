from datetime import datetime, timezone

def get_moment():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
