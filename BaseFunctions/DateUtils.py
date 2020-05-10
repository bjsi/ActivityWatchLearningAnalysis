import datetime as dt
from UnitAnalysis.SuperMemo.config import SM_MIDNIGHT


def n_hours_ago(h: int) -> dt.datetime:
    return (dt.datetime.now() -
            dt.timedelta(hours=h))


def n_days_ago(d: int) -> dt.datetime:
    day = dt.datetime.now() - dt.timedelta(days=d)
    return day.replace(hour=SM_MIDNIGHT.hour,
                       minute=SM_MIDNIGHT.minute,
                       second=SM_MIDNIGHT.second)


def n_weeks_ago(w: int) -> dt.datetime:
    week = dt.datetime.now() - dt.timedelta(days=(w * 7))
    return week.replace(hour=SM_MIDNIGHT.hour,
                        minute=SM_MIDNIGHT.minute,
                        second=SM_MIDNIGHT.second)

