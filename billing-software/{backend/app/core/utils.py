# core/utils.py
from datetime import datetime
from zoneinfo import ZoneInfo

IST_ZONE = ZoneInfo("Asia/Kolkata")

def to_ist(dt: datetime) -> datetime:
    """
    Converts a UTC datetime object to IST timezone.
    Assumes dt is timezone-naive UTC or timezone-aware UTC.
    Returns timezone-aware IST datetime.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # assume UTC
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(IST_ZONE)
