from asq import query
from asq.extension import extend
from asq.queryables import Queryable
from asq.selectors import a_, aq_, m_
from BaseFunctions.QueryHelpers import apply, where, order_by, count


@extend(Queryable)
def order_topics_by_insertions(q: Queryable):
    """
    Number of insertions.
    """
    return apply([
        where(a_('is_topic')),
        order_by(a_('inserted_diffs').count())
    ], q)


@extend(Queryable)
def order_topics_by_insertion_length(q: Queryable):
    """
    Text Length.
    """
    return apply([
        where(a_('is_topic')),
        order_by(query(a_('inserted_diffs')).sum(lambda x: len(x[1])))
    ])


@extend(Queryable)
def order_topics_by_deletions(q: Queryable):
    """
    Number of deletions.
    """
    return apply([
        # where(a_('is_topic')),
        order_by(lambda x: len(x.deleted_diffs))
    ], q)


@extend(Queryable)
def order_topics_by_deletion_length(q: Queryable):
    """
    Text length.
    """
    return apply([
        # where(a_('is_topic')),
        order_by(lambda x: len(diff[1] for diff in x.deleted_diffs))
    ], q)

