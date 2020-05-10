from enum import Enum


# None is reserved keyword
class LearningMode(Enum):
    none = 0,
    Standard = 1,
    Forced = 2,
    Neural = 3,
    Subset = 4,
    ForceSubset = 5,
    ForceTopics = 6,
    RandomTest = 7,
    DesignerTest = 8,
    Pending = 9,
    Drill = 10


class ElementType(Enum):
    Topic = 0
    Item = 1
    Task = 2
    Template = 3
    ConceptGroup = 4

