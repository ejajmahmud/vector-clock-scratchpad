"""Core Vector Clock Scratchpad implementation."""
import copy
from typing import Dict, List, Optional, Any


class CausalNote:
    def __init__(self, note_id: str, author: str, content: str, clock: Dict[str, int]):
        self.note_id = note_id
        self.author = author
        self.content = content
        self.clock = dict(clock)


class VectorClockScratchpad:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = {node_id: 0}
        self.notes: Dict[str, CausalNote] = {}

    def write_note(self, note_id: str, content: str) -> CausalNote:
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
        note = CausalNote(note_id, self.node_id, content, self.clock)
        self.notes[note_id] = note
        return note

    def compare_clocks(self, c1: Dict[str, int], c2: Dict[str, int]) -> str:
        """Returns: 'BEFORE', 'AFTER', 'EQUAL', or 'CONCURRENT'."""
        all_keys = set(c1.keys()).union(set(c2.keys()))
        le = True
        ge = True
        for k in all_keys:
            v1 = c1.get(k, 0)
            v2 = c2.get(k, 0)
            if v1 > v2:
                le = False
            if v1 < v2:
                ge = False

        if le and ge:
            return "EQUAL"
        if le:
            return "BEFORE"
        if ge:
            return "AFTER"
        return "CONCURRENT"

    def merge_remote(self, remote_scratchpad: "VectorClockScratchpad") -> List[str]:
        conflicts = []
        # Update clock with pairwise maximum
        for node, val in remote_scratchpad.clock.items():
            self.clock[node] = max(self.clock.get(node, 0), val)

        for note_id, remote_note in remote_scratchpad.notes.items():
            if note_id not in self.notes:
                self.notes[note_id] = remote_note
            else:
                rel = self.compare_clocks(self.notes[note_id].clock, remote_note.clock)
                if rel == "BEFORE":
                    self.notes[note_id] = remote_note
                elif rel == "CONCURRENT":
                    conflicts.append(note_id)
        return conflicts
