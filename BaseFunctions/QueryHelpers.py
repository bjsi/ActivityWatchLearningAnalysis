from typing import List, Callable, Any
from asq import query
from asq.queryables import Queryable, Grouping
from asq.selectors import a_, m_
from enum import Enum


class Order(Enum):
    Asc = 0
    Desc = 1


def apply(filters: List[Callable], q: Queryable) -> Queryable:
    """
    Apply a list of functions to a queryable object.
    :param filters:
    :param q:
    :return:
    """
    for f in filters:
        q = f(q)
    return q


def then_by(selector: Callable):
    return lambda x: x.then_by(selector)


def where(f: Callable[[Any], bool]):
    return lambda x: x.where(f)


def select(f: Callable):
    return lambda x: x.select(f)


def group_by(selector):
    return lambda x: x.group_by(selector)


def order_by(selector):
    return lambda x: x.order_by_descending(selector)


def get_sum(selector: Callable):
    return lambda x: x.sum(selector)


def lst(x):
    return x.last()


def fst(x):
    return x.first()


def count(x):
    return lambda x: x.count()


def order_grouping_by(selector: Callable, type: Order = Order.Asc):
    """
    subselect the group items within each grouping.
    """
    asc = lambda x: x.order_by(lambda y: query(y).select(selector).sum())
    desc = lambda x: x.order_by_descending(lambda y: query(y).select(selector).sum())
    return asc if type == Order.Asc else desc


order_by_duration = order_by(get_sum(a_('duration')))
group_by_category = group_by(a_('parent_category'))
group_by_concept = group_by(a_('data.concept_name'))
group_by_collection = group_by(a_('data.collection_name'))
group_by_date = group_by(m_('date'))
group_by_learning_mode = group_by(a_('data.learning_mode'))
group_by_element_type = group_by(a_('data.element_type'))
group_by_edited = group_by(m_('was_edited'))

#order_by_deletion_number = order_by(lambda x: text_deletions(x.data.element_content).count())
#order_by_insertion_number = order_by(lambda x: text_insertions(x.data.element_content).count())
#order_by_deletion_length = order_by(lambda x: text_insertions(x.data.element_content).sum())
#order_by_insertion_length = order_by(lambda x: sum(len(tup[1]) for tup in text_insertions(x.data.element_content)))
