from typing import List, Tuple, Dict, Any
import json
from aw_core.models import _timestamp_parse
from diff_match_patch import diff_match_patch
from .Enums import LearningMode, ElementType
from .Records import TabulateMixin
import datetime as dt


class Element:

    element_id: int
    element_title: str
    learning_mode: "LearningMode"
    concept_id: id
    concept_name: str
    element_type: "ElementType"
    deleted: bool
    children_delta: int
    collection_name: str
    element_content: List[Tuple[int, str]]
    category_path: List[str]
    full_path: List[str]

    def __init__(self, data: Dict[str, Any]):
        self.element_id = data["element_id"]
        self.element_title = data["element_title"]
        self.learning_mode = LearningMode[data["learning_mode"].lower()
                                       if data["learning_mode"] == "None"
                                       else data["learning_mode"]]
        self.concept_id = data["concept_id"]
        self.concept_name = data["concept_name"]
        self.element_type = ElementType[data["element_type"]]
        self.deleted = data["deleted"]
        self.collection_name = data["collection_name"]
        self.element_content = self.json_to_dmp_format(data["element_content"])
        self.category_path = data["category_path"]
        self.full_path = data["full_path"]
        self.children_delta = data["children_delta"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_id": self.element_id,
            "element_title": self.element_title,
            "learning_mode": (self.learning_mode.name
                              if self.learning_mode != LearningMode.none
                              else "None"),
            "concept_id": self.concept_id,
            "concept_name": self.concept_name,
            "element_type": self.element_type.name,
            "deleted": self.deleted,
            "children_delta": self.children_delta,
            "collection_name": self.collection_name,
            "element_content": self.element_content,
            "category_path": self.category_path,
            "full_path": self.full_path
        }


    @staticmethod
    def json_to_dmp_format(content: str):
        json_content = json.loads(content)
        return [
            (int(k), v)
            for dic in json_content
            for k, v in dic.items()
        ]


class SMEvent(TabulateMixin):

    id: int
    timestamp: dt.datetime
    duration: dt.timedelta
    data: Element

    def __init__(self, id, timestamp, duration, data):
        self.duration = duration
        self.data = Element(data)
        self.id = id
        self.timestamp = _timestamp_parse(timestamp)

    def date(self):
        return self.timestamp.date()

    @property
    def is_item(self) -> bool:
        return self.data.element_type == ElementType.Item

    @property
    def is_concept(self) -> bool:
        return self.data.element_type == ElementType.ConceptGroup

    @property
    def is_topic(self) -> bool:
        return self.data.element_type == ElementType.Topic

    @property
    def parent_category(self):
        return self.data.category_path[0] if self.data.category_path else None

    @property
    def has_insertions(self) -> bool:
        return any(diff[0] == 1 for diff in self.data.element_content)

    @property
    def has_deletions(self) -> bool:
        return any(diff[0] == -1 for diff in self.data.element_content)

    def inserted_contains(self, strings: List[str]) -> bool:
        return any(
            any(string in diff[1] for string in strings)
            for diff in self.data.element_content
            if diff[0] == 1
        )

    def unchanged_contains(self, strings: List[str]) -> bool:
        return any(
            any(string in diff[1] for string in strings)
            for diff in self.data.element_content
            if diff[0] == 0
        )

    def deleted_contains(self, strings: List[str]) -> bool:
        return any(
            any(string in diff[1] for string in strings)
            for diff in self.data.element_content
            if diff[0] == -1
        )

    @property
    def during_review(self) -> bool:
        return self.data.learning_mode != LearningMode.none

    @property
    def during_drill(self) -> bool:
        return self.data.learning_mode == LearningMode.Drill

    @property
    def during_standard(self):
        return self.data.learning_mode == LearningMode.Standard

    @property
    def edited(self) -> bool:
        return any(diff[0] != 0 for diff in self.data.element_content)

    # Element content manipulation
    @property
    def diff_text1(self) -> str:
        dmp = diff_match_patch()
        return dmp.diff_text1(self.data.element_content)

    @property
    def diff_text2(self) -> str:
        dmp = diff_match_patch()
        return dmp.diff_text2(self.data.element_content)

    def diff_html(self) -> str:
        dmp = diff_match_patch()
        return dmp.diff_prettyHtml(self.data.element_content)

    @property
    def unchanged_diffs(self) -> List:
        return [
            diff for diff in self.data.element_content
            if diff[0] == 1
        ]

    @property
    def inserted_diffs(self) -> List:
        return [
            diff for diff in self.data.element_content
            if diff[0] == 1
        ]

    @property
    def deleted_diffs(self) -> List:
        return [
            diff for diff in self.data.element_content
            if diff[0] == -1
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "data": self.data.to_dict()
        }

    def __repr__(self):
        return f"<SMEvent: duration: {self.duration} title: {self.data.element_title[0:15]}>"
