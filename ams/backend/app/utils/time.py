from datetime import datetime
from zoneinfo import ZoneInfo


def now_in(tz_name: str) -> datetime:
    """Current time in the school's timezone (see SchoolSetting.timezone)."""
    return datetime.now(ZoneInfo(tz_name))
