from asq.extension import extend
from asq.selectors import a_
from BaseFunctions.BaseClient import get_sm_events
from asq.queryables import Grouping, Queryable
from BaseFunctions.DateUtils import *
from BaseFunctions.QueryHelpers import group_by_collection, order_grouping_by, fst, apply, Order, select
from UnitAnalysis.SuperMemo.Models.Records import Collection


@extend(Grouping)
def as_collection(g: Grouping) -> Collection:
    return Collection(name=g.key, time=g.sum(lambda x: x.duration))


@extend(Queryable)
def get_top_collection(q: Queryable) -> Queryable:
    return apply([
        group_by_collection,
        order_grouping_by(a_('duration'), Order.Desc),
        fst,
        as_collection
    ], q)


@extend(Queryable)
def get_collection_times(q: Queryable) -> Queryable:
    return apply([
        group_by_collection,
        order_grouping_by(a_('duration'), Order.Desc),
        select(lambda x: as_collection(x))
    ], q)


if __name__ == "__main__":
    events = get_sm_events(n_days_ago(2), n_days_ago(0))
    print(events.get_collection_times().tabulate())


