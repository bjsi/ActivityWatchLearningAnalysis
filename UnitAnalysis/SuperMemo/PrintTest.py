from typing import NamedTuple, Callable
from asq import query
from asq.extension import extend
from asq.queryables import Queryable
from treelib import Tree
from BaseFunctions.DateUtils import *


class NodeOptions(NamedTuple):
    transformation: Callable


# TODO: Combine methods, use a path selector
@extend(Queryable)
def treeify_category_path(q: Queryable) -> None:
    tree = Tree()
    events = q.to_list()
    for event in events:
        path = list(reversed(event.data.category_path))
        for idx, node_name in enumerate(path):
            if tree.get_node(node_name):
                continue
            parent = path[idx-1] if idx > 0 else None
            parent_node = tree.get_node(parent)
            tree.create_node(f"{node_name} time={query(events).where(lambda x: node_name in x.data.category_path).sum(lambda y: y.duration) // 1}",
                             node_name,
                             parent_node)
    tree.show(line_type="ascii-em")


@extend(Queryable)
def treeify_full_path(q: Queryable) -> None:
    tree = Tree()
    events = q.to_list()
    for event in events:
        path = list(reversed(event.data.full_path))
        for idx, node in enumerate(path):
            if tree.get_node(node):
                continue
            parent = path[idx - 1] if idx > 0 else None
            parent_node = tree.get_node(parent)
            tree.create_node(node, node, parent_node)
    tree.show(line_type="ascii-em")


