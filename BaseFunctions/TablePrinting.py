from typing import List, Optional, Callable, NamedTuple, Any
from asq.selectors import *
from asq.queryables import Queryable
from asq.extension import extend
from tabulate import tabulate as Tabulate


class RowOptions(NamedTuple):
    transformation: Optional[Callable]
    attribute_path: str
    column_heading: str


basic = [
    RowOptions(None, "id", "Event ID"),
    RowOptions(None, "duration", "Event Duration")
]


def print_table(q, row_ops: List[RowOptions]):
    rows = query(q).select(m_('to_table_row', row_ops))
    headers = [header for _, _, header in row_ops]
    print(Tabulate(rows, headers, tablefmt="grid", showindex="True"))


@extend(Queryable)
def tabulate(q: Queryable, row_ops: List[RowOptions] = basic):
    print_table(q, row_ops)


class TabulateMixin(object):

    def to_table_row(self, key_funcs: List[RowOptions]) -> List[List[Any]]:
        """
        Converts to a table of data suitable for tabulate to display.
        """

        # TODO: Refactor to allow m_
        return [
            func(a_(path)(self)) if func else a_(path)(self)
            for func, path, _ in key_funcs
        ]

