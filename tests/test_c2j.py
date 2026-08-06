"""Unit verification C2J (T-0046). Run: python -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from datakonv.c2j import csv_to_json  # noqa: E402
from datakonv.errors import DataError  # noqa: E402
import json  # noqa: E402


def parse(text, **kw):
    return json.loads(csv_to_json(text, **kw))


class ShapeTest(unittest.TestCase):
    def test_array_of_objects_with_header_keys(self):
        """First record is the header; output is an array of objects. Verifiziert: SWR-D05."""
        self.assertEqual(parse("name,age\nAnna,30\n"),
                         [{"name": "Anna", "age": 30}])

    def test_key_order_follows_columns(self):
        """Object keys preserve CSV column order. Verifiziert: SWR-D05."""
        text = csv_to_json("b,a,c\n1,2,3\n")
        self.assertLess(text.index('"b"'), text.index('"a"'))
        self.assertLess(text.index('"a"'), text.index('"c"'))

    def test_missing_header_is_data_error(self):
        """Empty input (no header record) is rejected. Verifiziert: SWR-D05."""
        with self.assertRaises(DataError):
            csv_to_json("")


class TypingTest(unittest.TestCase):
    def test_typing_table(self):
        """Numbers, booleans, null, and strings are typed deterministically. Verifiziert: SWR-D06."""
        row = parse("a,b,c,d,e,f,g\n30,3.5,1e3,TRUE,false,,abc\n")[0]
        self.assertEqual(row, {"a": 30, "b": 3.5, "c": 1000.0, "d": True,
                               "e": False, "f": None, "g": "abc"})

    def test_non_json_number_forms_stay_strings(self):
        """Leading zeros and non-grammar forms stay strings. Verifiziert: SWR-D06."""
        row = parse("a,b,c\n01,+5,1.\n")[0]
        self.assertEqual(row, {"a": "01", "b": "+5", "c": "1."})


class QuotingTest(unittest.TestCase):
    def test_rfc4180_quoting(self):
        """Quoted fields with embedded delimiter, escaped quote, and newline parse correctly. Verifiziert: SWR-D07."""
        row = parse('a,b,c\n"x,y","he said ""hi""","line1\nline2"\n')[0]
        self.assertEqual(row, {"a": "x,y", "b": 'he said "hi"', "c": "line1\nline2"})


class ErrorTest(unittest.TestCase):
    def test_field_count_mismatch_names_record(self):
        """A record with deviating field count fails with the record number. Verifiziert: SWR-D08."""
        with self.assertRaises(DataError) as k:
            csv_to_json("a,b\n1,2\n3\n")
        self.assertIn("record 3", str(k.exception))

    def test_duplicate_header_rejected(self):
        """Duplicate header names are rejected naming the column. Verifiziert: SWR-D09."""
        with self.assertRaises(DataError) as k:
            csv_to_json("a,a\n1,2\n")
        self.assertIn("column 2", str(k.exception))

    def test_empty_header_rejected(self):
        """Empty header names are rejected naming the column. Verifiziert: SWR-D09."""
        with self.assertRaises(DataError) as k:
            csv_to_json("a,,c\n1,2,3\n")
        self.assertIn("column 2", str(k.exception))


class IndentTest(unittest.TestCase):
    def test_compact_single_line(self):
        """indent=0 produces compact single-line JSON. Verifiziert: SWR-D18."""
        out = csv_to_json("a,b\n1,x\n", indent=0)
        self.assertEqual(out, '[{"a":1,"b":"x"}]\n')

    def test_custom_indent_width(self):
        """indent=n pretty-prints with n spaces; default stays 2. Verifiziert: SWR-D18."""
        self.assertIn('\n    "a"', csv_to_json("a\n1\n", indent=4))
        self.assertIn('\n  "a"', csv_to_json("a\n1\n"))


class DeterminismTest(unittest.TestCase):
    def test_double_run_byte_identical(self):
        """Identical input produces byte-identical output. Verifiziert: SWR-D16."""
        text = "a,b\n1,x\n2,y\n"
        self.assertEqual(csv_to_json(text), csv_to_json(text))


if __name__ == "__main__":
    unittest.main()
