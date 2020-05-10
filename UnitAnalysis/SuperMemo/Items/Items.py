from asq.extension import extend
from asq.queryables import Queryable
from BaseFunctions.BaseClient import get_sm_events
from BaseFunctions.Predicates import And
from BaseFunctions.QueryHelpers import apply, where, select
from BaseFunctions.TablePrinting import RowOptions
from asq.selectors import a_
from BaseFunctions.DiffHelpers import dmp
from UnitAnalysis.SuperMemo.ElementContent import fmt_el_content
from UnitAnalysis.SuperMemo.SMDateUtils import n_sm_days_ago


items_diff = [
    RowOptions(lambda x: x.strftime("%Y-%m-%d"), "timestamp", "Timestamp"),
    RowOptions(lambda x: x // 1, "duration", "Duration"),
    RowOptions(lambda x: fmt_el_content(dmp.diff_prettyHtml(x)), "data.element_content", "Diff"),
]

items_ba = [
    RowOptions(lambda x: x.strftime("%Y-%m-%d"), "timestamp", "Timestamp"),
    RowOptions(lambda x: x // 1, "duration", "Duration"),
    RowOptions(lambda x: fmt_el_content(dmp.diff_text1(x)), "data.element_content", "Before"),
    RowOptions(lambda x: fmt_el_content(dmp.diff_text2(x)), "data.element_content", "After")
]


@extend(Queryable)
def items_edited_during_drill(q: Queryable):
    return apply([
        where(And(a_('is_item'), a_('edited'), a_('during_drill'))),
    ], q)


@extend(Queryable)
def items_edited_during_standard(q: Queryable):
    return apply([
        where(And(a_('is_item'), a_('edited'), a_('during_standard'))),
    ], q)



if __name__ == '__main__':
    events = get_sm_events(n_sm_days_ago(2), n_sm_days_ago(0))
    events.items_edited_during_standard().tabulate(row_ops=items_ba)
