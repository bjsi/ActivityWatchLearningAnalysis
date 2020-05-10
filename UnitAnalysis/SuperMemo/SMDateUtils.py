from BaseFunctions.DateUtils import n_days_ago, n_weeks_ago
from .config import SM_MIDNIGHT


def n_sm_days_ago(n: int):
    day = n_days_ago(n)
    return day.replace(hour=SM_MIDNIGHT.hour,
                       minute=SM_MIDNIGHT.minute,
                       second=SM_MIDNIGHT.second)


def n_sm_weeks_ago(n: int):
    week = n_weeks_ago(n)
    return week.replace(hour=SM_MIDNIGHT.hour,
                        minute=SM_MIDNIGHT.minute,
                        second=SM_MIDNIGHT.second)


