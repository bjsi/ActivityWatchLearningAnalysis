from asq.queryables import Queryable
from aw_client import ActivityWatchClient
from typing import List, Dict, Callable
from BaseFunctions.QueryHelpers import apply
from UnitAnalysis.SuperMemo.config import SM_BUCKET_NAME
import datetime as dt
from UnitAnalysis.SuperMemo.Models.SMEvent import SMEvent
from asq import query
from functools import partial


# TODO: Add Aw-Transformation functions
class ExtendedActivityWatchClient(ActivityWatchClient):

    def __init__(self):
        super().__init__(testing=True)

    def get_sm_events(self, start: dt.datetime, end: dt.datetime, filters: List[Callable], limit: int = -1) -> Queryable:

        endpoint = f"buckets/{SM_BUCKET_NAME}/events"
        params: Dict[str, str] = dict()

        if limit is not None:
            params["limit"] = str(limit)
        if start is not None:
            params["start"] = start.isoformat()
        if end is not None:
            params["end"] = end.isoformat()
        aw_events = self._get(endpoint, params=params).json()
        sm_events = [SMEvent(**event) for event in aw_events]
        return apply(filters, query(sm_events))


ea = ExtendedActivityWatchClient()
get_sm_events = partial(ea.get_sm_events, filters=[], limit=-1)


