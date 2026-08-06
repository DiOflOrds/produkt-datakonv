"""Unit verification CLI (T-0046). Run: python -m unittest discover -s tests"""
import contextlib
import io
import os
import sys
import tempfile
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from datakonv import cli  # noqa: E402


def run(argv, stdin_text=None, stdin_bytes=None):
    """Run cli.main with captured stdio. Returns (exit_code, stdout, stderr)."""
    alt_in = sys.stdin
    out, err = io.StringIO(), io.StringIO()
    if stdin_bytes is not None:
        sys.stdin = types.SimpleNamespace(buffer=io.BytesIO(stdin_bytes))
    elif stdin_text is not None:
        sys.stdin = io.StringIO(stdin_text)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = cli.main(argv)
    finally:
        sys.stdin = alt_in
    return rc, out.getvalue(), err.getvalue()


class DirectionTest(unittest.TestCase):
    def test_missing_to_is_usage_error(self):
        """Missing --to exits 2 with a usage message on stderr. Verifiziert: SWR-D01, SWR-D15."""
        rc, out, err = run(["-"], stdin_text="a\n1\n")
        self.assertEqual(rc, 2)
        self.assertEqual(out, "")
        self.assertNotEqual(err, "")

    def test_invalid_to_value_is_usage_error(self):
        """Invalid --to value exits 2. Verifiziert: SWR-D01."""
        rc, _, _ = run(["--to", "xml", "-"], stdin_text="a\n1\n")
        self.assertEqual(rc, 2)


class IoTest(unittest.TestCase):
    def test_stdin_to_stdout(self):
        """Omitted path reads stdin; omitted --out writes stdout. Verifiziert: SWR-D02."""
        rc, out, err = run(["--to", "json"], stdin_text="a\n1\n")
        self.assertEqual((rc, err), (0, ""))
        self.assertIn('"a": 1', out)

    def test_file_to_file(self):
        """File input and --out file output work. Verifiziert: SWR-D02."""
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "in.csv")
            dst = os.path.join(d, "out.json")
            open(src, "w", encoding="utf-8").write("a\n1\n")
            rc, out, _ = run(["--to", "json", src, "--out", dst])
            self.assertEqual((rc, out), (0, ""))
            self.assertIn('"a": 1', open(dst, encoding="utf-8").read())

    def test_unreadable_input_is_data_error(self):
        """Nonexistent input file exits 3. Verifiziert: SWR-D02, SWR-D15."""
        rc, _, err = run(["--to", "json", "/nope/missing.csv"])
        self.assertEqual(rc, 3)
        self.assertIn("cannot read input", err)


class DelimiterTest(unittest.TestCase):
    def test_delimiter_applies_to_input_and_output(self):
        """--delimiter is used for CSV input and output. Verifiziert: SWR-D03."""
        rc, out, _ = run(["--to", "json", "--delimiter", ";"], stdin_text="a;b\n1;2\n")
        self.assertEqual(rc, 0)
        self.assertIn('"b": 2', out)
        rc, out, _ = run(["--to", "csv", "--delimiter", ";"],
                         stdin_text='[{"a": 1, "b": 2}]')
        self.assertEqual((rc, out), (0, "a;b\n1;2\n"))

    def test_multichar_delimiter_is_usage_error(self):
        """A multi-character delimiter exits 2. Verifiziert: SWR-D03."""
        rc, _, err = run(["--to", "json", "--delimiter", ";;"], stdin_text="a\n1\n")
        self.assertEqual(rc, 2)
        self.assertIn("single character", err)


class ConventionTest(unittest.TestCase):
    def test_help_exits_0_on_stdout(self):
        """--help prints to stdout and exits 0. Verifiziert: SWR-D04."""
        rc, out, err = run(["--help"])
        self.assertEqual((rc, err), (0, ""))
        self.assertIn("usage", out)

    def test_version_exits_0_on_stdout(self):
        """--version prints to stdout and exits 0. Verifiziert: SWR-D04."""
        rc, out, err = run(["--version"])
        self.assertEqual((rc, err), (0, ""))
        self.assertIn("datakonv", out)


class EncodingTest(unittest.TestCase):
    def test_utf8_round_trip(self):
        """UTF-8 content (umlauts) survives conversion. Verifiziert: SWR-D14."""
        rc, out, _ = run(["--to", "json"], stdin_text="stadt\nKöln\n")
        self.assertEqual(rc, 0)
        self.assertIn("Köln", out)

    def test_bom_input_is_stripped(self):
        """A leading UTF-8 BOM is stripped; header keys stay clean (regression T-0053). Verifiziert: SWR-D14."""
        rc, out, _ = run(["--to", "json"], stdin_bytes=b"\xef\xbb\xbfa\nx\n")
        self.assertEqual(rc, 0)
        self.assertIn('"a"', out)

    def test_invalid_utf8_is_data_error(self):
        """Input that is not valid UTF-8 exits 3. Verifiziert: SWR-D14, SWR-D15."""
        rc, out, err = run(["--to", "json"], stdin_bytes=b"a\n\xff\xfe\n")
        self.assertEqual((rc, out), (3, ""))
        self.assertIn("UTF-8", err)


class ExitCodeTest(unittest.TestCase):
    def test_data_error_never_writes_stdout(self):
        """Diagnostics go to stderr only; stdout stays empty on errors. Verifiziert: SWR-D15."""
        rc, out, err = run(["--to", "json"], stdin_text="a,b\n1\n")
        self.assertEqual((rc, out), (3, ""))
        self.assertIn("record", err)

    def test_unexpected_exception_exits_1(self):
        """Unexpected internal errors exit 1 with stderr diagnostic. Verifiziert: SWR-D15."""
        with mock.patch.object(cli, "csv_to_json", side_effect=RuntimeError("boom")):
            rc, out, err = run(["--to", "json"], stdin_text="a\n1\n")
        self.assertEqual((rc, out), (1, ""))
        self.assertIn("internal error", err)


if __name__ == "__main__":
    unittest.main()
