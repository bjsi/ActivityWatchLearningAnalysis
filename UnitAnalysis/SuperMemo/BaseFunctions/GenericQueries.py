from typing import List

from asq.extension import extend
from asq.queryables import Queryable
from asq.selectors import m_, a_

from BaseFunctions.BaseClient import get_sm_events
from BaseFunctions.QueryHelpers import apply, where, order_by
from BaseFunctions.TablePrinting import RowOptions
from BaseFunctions.TextHelpers import short
from UnitAnalysis.SuperMemo.BaseFunctions.TextAnalysis import get_entities
from UnitAnalysis.SuperMemo.SMDateUtils import n_sm_days_ago

generic = [
    RowOptions(lambda x: short(x, 30), "data.element_title", "Element Title"),
    RowOptions(lambda x: x.strftime("%Y-%m-%d"), "timestamp", "Timestamp"),
    RowOptions(None, "data.collection_name", "Collection"),
    RowOptions(lambda x: x[0], "data.category_path", "Category"),
    # RowOptions(None, "data.children_delta", "Net Children Added")
    # RowOptions(lambda x: get_entities(x), 'diff_text1', "Text1 Entities")
]


show_entities = [
]


@extend(Queryable)
def order_by_insertions(q: Queryable):
    """
    Number of insertions.
    """
    return apply([
        order_by(lambda x: len(x.inserted_diffs))
    ], q)


@extend(Queryable)
def order_by_insertion_length(q: Queryable):
    """
    Text Length.
    """
    return apply([
        order_by(lambda x: sum(len(diff[1]) for diff in x.inserted_diffs))
    ], q)


@extend(Queryable)
def order_by_deletions(q: Queryable):
    """
    Number of deletions.
    """
    return apply([
        order_by(lambda x: len(x.deleted_diffs))
    ], q)


@extend(Queryable)
def order_by_deletion_length(q: Queryable):
    """
    Text length.
    """
    return apply([
        order_by(lambda x: sum(len(diff[1]) for diff in x.deleted_diffs))
    ], q)


@extend(Queryable)
def order_by_child_delta(q: Queryable):
    return apply([
        order_by(a_('data.children_delta'))
    ], q)


@extend(Queryable)
def where_deleted_contains(q: Queryable, string: str):
    return apply([
        where(m_('deleted_contains', string))
    ], q)


@extend(Queryable)
def where_inserted_contains(q: Queryable, strings: List[str]):
    return apply([
        where(m_('inserted_contains', strings))
    ], q)


@extend(Queryable)
def where_unchanged_contains(q: Queryable, string: str):
    return apply([
        where(m_('unchanged_contains', string))
    ], q)


if __name__ == '__main__':
    events = get_sm_events(n_sm_days_ago(1), n_sm_days_ago(0))
    events.where(a_('is_topic')).where_inserted_contains(["Why", "why"]).tabulate(generic)