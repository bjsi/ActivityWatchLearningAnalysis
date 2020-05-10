import datetime as dt
from UnitAnalysis.SuperMemo.Models import LearningMode
from typing import Dict, Optional
from collections import defaultdict


def top_learning_mode():
    pass




    def get_learning_modes(self, start: dt.datetime, end: dt.datetime) -> Dict[str, dt.timedelta]:
        events = self.get_events(start, end)
        dic = defaultdict(dt.timedelta)
        for event in events:
            dic[event.data["learning_mode"]] += event.duration
        return dic

    def get_top_learning_mode(self, start: dt.datetime, end: dt.datetime):
        dic = self.get_learning_modes(start, end)
        top = max(dic, key=dic.get)
        return LearningModeTime(mode=LearningMode[top.title()], time=dic[top])

    def get_learning_mode(self, mode: LearningMode, start: dt.datetime, end: dt.datetime) -> Optional[LearningModeTime]:
        learning_modes = self.get_learning_modes()
        if not learning_modes:
            return
        learning_mode = learning_modes.get(mode.name.title())
        if not mode:
            return
        return LearningModeTime(mode=mode, time=learning_modes[mode.name.title()])

    def print_learning_mode_table(self, start: dt.datetime, end: dt.datetime) -> None:

        learning_modes = self.get_learning_modes(start, end)

        if not learning_modes:
            return

        learning_modes = list(learning_modes.items())
        learning_modes.sort(key=lambda x: x[1], reverse=True)

        print(f"Learning Mode Timetable for Range {start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')}")
        for k, v in learning_modes:
            print(f"{k}\t\t\t{v}")

