"""Unit tests for vector-clock-scratchpad."""
import unittest
from vector_clock_scratchpad.scratchpad import VectorClockScratchpad


class TestVectorClockScratchpad(unittest.TestCase):
    def test_local_write_increments_clock(self):
        s = VectorClockScratchpad("a1")
        note = s.write_note("n1", "Hello")
        self.assertEqual(note.clock["a1"], 1)
        self.assertEqual(s.clock["a1"], 1)

    def test_causal_ordering(self):
        s1 = VectorClockScratchpad("a1")
        s2 = VectorClockScratchpad("a2")
        c1 = {"a1": 1, "a2": 0}
        c2 = {"a1": 2, "a2": 0}
        self.assertEqual(s1.compare_clocks(c1, c2), "BEFORE")
        self.assertEqual(s1.compare_clocks(c2, c1), "AFTER")

    def test_concurrent_detection(self):
        s1 = VectorClockScratchpad("a1")
        c1 = {"a1": 1, "a2": 0}
        c2 = {"a1": 0, "a2": 1}
        self.assertEqual(s1.compare_clocks(c1, c2), "CONCURRENT")
