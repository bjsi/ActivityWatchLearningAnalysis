from typing import List
from abc import ABC
import datetime as dt
from BaseFunctions.TablePrinting import print_table, RowOptions, TabulateMixin
from UnitAnalysis.SuperMemo.PrintTest import NodeOptions


class Record(ABC, TabulateMixin):

    name: str
    time: dt.timedelta

    # For tabulate printing
    default_row_options: List[RowOptions]
    # For tree printing
    default_node_options: List[NodeOptions]

    def tabulate(self, row_ops=None):
        print_table([self], row_ops if row_ops else self.default_row_options)

    def treeify(self, tree_ops=None):
        pass


class Category(Record):

    default_row_options = [
        RowOptions(None, "name", "Category Name"),
        RowOptions(lambda x: x // 1, "time", "Time (s)")
    ]

    def __init__(self, name: str, time: float):
        self.name = name
        self.time = time

    def __repr__(self):
        return f"<Category: name=\'{self.name}\' time={self.time}>"


class Item(Record):

    # TODO
    default_row_options = [
    ]

    def __init__(self, name: str, time: float):
        self.name = name
        self.time = time

    def __repr__(self):
        return f"<Item: name=\'{self.name}\' time={self.time}>"


class Topic(Record):

    # TODO:
    default_row_options = [

    ]

    def __init__(self, name: str, time: str):
        self.name = name
        self.time = time

    def __repr__(self):
        return f"<Topic: name=\'{self.name}\' time={self.time}>"


class Collection(Record):

    default_row_options = [
        RowOptions(None, "name", "Collection Name"),
        RowOptions(lambda x: x // 1, "time", "Time (s)")
    ]

    def __init__(self, name: str, time: dt.timedelta):
        self.name = name
        self.time = time

    def __repr__(self):
        return f"<Collection: name=\'{self.name}\' time={self.time}>"


