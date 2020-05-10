from asq.extension import extend
from asq.selectors import a_

from BaseFunctions.BaseClient import get_sm_events
from BaseFunctions.DateUtils import *
from BaseFunctions.QueryHelpers import apply, group_by_category, fst, select, order_grouping_by, Order
from UnitAnalysis.SuperMemo.Models.Records import Category
from asq.queryables import Grouping, Queryable


@extend(Grouping)
def as_category(g: Grouping) -> Category:
    return Category(name=g.key, time=g.sum(lambda x: x.duration))


@extend(Queryable)
def get_top_category(q: Queryable) -> Queryable:
    return apply([
        group_by_category,
        order_grouping_by(a_('duration'), Order.Desc),
        fst,
        as_category
    ], q)


@extend(Queryable)
def get_bottom_category(q: Queryable) -> Queryable:
    return apply([
        group_by_category,
        order_grouping_by(a_('duration'), Order.Asc),
        fst,
        as_category
    ], q)


@extend(Queryable)
def order_categories_by_time(q: Queryable) -> Queryable:
    return apply([
        group_by_category,
        order_grouping_by(a_('duration'), Order.Desc),
        select(lambda x: Category(name=x.key, time=x.sum(a_('duration'))))
    ], q)


if __name__ == "__main__":
    events = get_sm_events(n_days_ago(2), n_days_ago(0))
    events.get_top_category().tabulate()


