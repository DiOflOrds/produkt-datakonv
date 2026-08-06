"""System/integration verification (SWE.5/6, T-0052): the real CLI as subprocess —
files, pipes, exit codes, realistic inputs. Complements unit level (T-0046)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_cli(args, stdin_bytes=b""):
    env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"))
    p = subprocess.run([sys.executable, "-m", "datakonv", *args],
                       input=stdin_bytes, capture_output=True, env=env, cwd=ROOT)
    return p.returncode, p.stdout, p.stderr


class PipelineTest(unittest.TestCase):
    def test_pipe_csv_to_json(self):
        """Shell-pipe style stdin→stdout works end to end. Verifiziert: SWR-D02, SWR-D05."""
        rc, out, err = run_cli(["--to", "json"], b"name,age\nAnna,30\n")
        self.assertEqual((rc, err), (0, b""))
        self.assertEqual(json.loads(out), [{"name": "Anna", "age": 30}])

    def test_file_to_file_roundtrip(self):
        """CSV→JSON→CSV over real files reproduces the original bytes. Verifiziert: SWR-D02, SWR-D17."""
        original = b"name,age,ok\nAnna,30,true\nBob,,false\n"
        with tempfile.TemporaryDirectory() as d:
            src, js, back = (os.path.join(d, n) for n in ("in.csv", "mid.json", "out.csv"))
            open(src, "wb").write(original)
            self.assertEqual(run_cli(["--to", "json", src, "--out", js])[0], 0)
            self.assertEqual(run_cli(["--to", "csv", js, "--out", back])[0], 0)
            self.assertEqual(open(back, "rb").read(), original)

    def test_semicolon_delimiter_end_to_end(self):
        """--delimiter is honored through the whole pipeline. Verifiziert: SWR-D03."""
        rc, out, _ = run_cli(["--to", "csv", "--delimiter", ";"],
                             b'[{"a": 1, "b": "x,y"}]')
        self.assertEqual((rc, out), (0, b"a;b\n1;x,y\n"))


class RobustnessTest(unittest.TestCase):
    def test_exit_codes_and_stream_separation(self):
        """Usage error 2, data error 3, diagnostics only on stderr. Verifiziert: SWR-D15."""
        rc, out, err = run_cli([], b"")
        self.assertEqual((rc, out), (2, b""))
        self.assertNotEqual(err, b"")
        rc, out, err = run_cli(["--to", "json"], b"a,b\n1\n")
        self.assertEqual((rc, out), (3, b""))
        self.assertIn(b"record", err)

    def test_umlauts_survive_utf8(self):
        """Non-ASCII UTF-8 content survives conversion byte-correctly. Verifiziert: SWR-D14."""
        rc, out, _ = run_cli(["--to", "json"], "stadt\nKöln\n".encode("utf-8"))
        self.assertEqual(rc, 0)
        self.assertIn("Köln", out.decode("utf-8"))

    def test_excel_bom_header_is_clean(self):
        """A leading UTF-8 BOM (Excel export) must not leak into the first header key. Verifiziert: SWR-D14."""
        rc, out, _ = run_cli(["--to", "json"], b"\xef\xbb\xbfname,age\nAnna,30\n")
        self.assertEqual(rc, 0)
        self.assertEqual(list(json.loads(out)[0].keys()), ["name", "age"])

    def test_version_end_to_end(self):
        """--version prints the tool version on stdout. Verifiziert: SWR-D04."""
        rc, out, err = run_cli(["--version"])
        self.assertEqual((rc, err), (0, b""))
        self.assertIn(b"datakonv", out)


if __name__ == "__main__":
    unittest.main()
