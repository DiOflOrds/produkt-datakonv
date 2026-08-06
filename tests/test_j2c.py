"""Unit verification J2C (T-0046). Run: python -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from datakonv.c2j import csv_to_json  # noqa: E402
from datakonv.errors import DataError  # noqa: E402
from datakonv.j2c import json_to_csv  # noqa: E402


class StructureTest(unittest.TestCase):
    def test_parse_error_distinguished(self):
        """Syntactically invalid JSON reports a parse error. Verifiziert: SWR-D10."""
        with self.assertRaises(DataError) as k:
            json_to_csv("{not json")
        self.assertIn("parse error", str(k.exception))

    def test_structure_error_distinguished(self):
        """Valid JSON with wrong top-level structure reports a structure error. Verifiziert: SWR-D10."""
        for text in ('{"a": 1}', '[1, 2]'):
            with self.assertRaises(DataError) as k:
                json_to_csv(text)
            self.assertIn("structure error", str(k.exception))


class HeaderTest(unittest.TestCase):
    def test_key_union_first_occurrence_order_and_missing_empty(self):
        """Header is the key union in first-occurrence order; missing keys yield empty fields. Verifiziert: SWR-D11."""
        out = json_to_csv('[{"b": 1, "a": 2}, {"a": 3, "c": 4}]')
        self.assertEqual(out, "b,a,c\n1,2,\n,3,4\n")


class SerializationTest(unittest.TestCase):
    def test_serialization_table(self):
        """Strings verbatim, numbers/booleans as JSON literals, null empty. Verifiziert: SWR-D12."""
        out = json_to_csv('[{"s": "x", "n": 3.5, "i": 7, "t": true, "z": null}]')
        self.assertEqual(out.splitlines()[1], "x,3.5,7,true,")

    def test_rfc4180_quoting_applied(self):
        """Fields containing delimiter, quote, or newline are quoted. Verifiziert: SWR-D12."""
        out = json_to_csv('[{"a": "x,y", "b": "he said \\"hi\\""}]')
        self.assertEqual(out.splitlines()[1], '"x,y","he said ""hi"""')


class NestingTest(unittest.TestCase):
    def test_nested_value_rejected_with_path(self):
        """Nested object/array values fail with the JSON path. Verifiziert: SWR-D13."""
        with self.assertRaises(DataError) as k:
            json_to_csv('[{"a": 1}, {"address": {"city": "X"}}]')
        self.assertIn("[1].address", str(k.exception))
        with self.assertRaises(DataError) as k:
            json_to_csv('[{"tags": [1, 2]}]')
        self.assertIn("[0].tags", str(k.exception))


class DeterminismTest(unittest.TestCase):
    def test_double_run_byte_identical(self):
        """Identical input produces byte-identical output. Verifiziert: SWR-D16."""
        text = '[{"a": 1, "b": "x"}]'
        self.assertEqual(json_to_csv(text), json_to_csv(text))

    def test_roundtrip_csv_json_csv(self):
        """CSV -> JSON -> CSV reproduces the original byte-identically. Verifiziert: SWR-D17."""
        original = "name,age,ok\nAnna,30,true\nBob,,false\n"
        self.assertEqual(json_to_csv(csv_to_json(original)), original)


if __name__ == "__main__":
    unittest.main()
