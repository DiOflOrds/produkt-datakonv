"""CLI unit: argument parsing, I/O wiring, central exit-code mapping (ADR-D03).

SWR reference: SWR-D01 (--to required), SWR-D02 (file/stdin/stdout),
SWR-D03 (--delimiter), SWR-D04 (--help/--version), SWR-D14 (UTF-8),
SWR-D15 (exit codes, diagnostics on stderr only).
"""
import argparse
import sys

from . import __version__
from .c2j import csv_to_json
from .errors import EXIT_DATA, EXIT_INTERNAL, EXIT_OK, EXIT_USAGE, DataError, UsageError
from .j2c import json_to_csv


def _parser():
    p = argparse.ArgumentParser(
        prog="datakonv",
        description="Convert CSV to JSON (array of objects) and JSON to CSV.")
    p.add_argument("--to", required=True, choices=("json", "csv"), dest="target",
                   help="conversion target format")
    p.add_argument("input", nargs="?", default="-",
                   help="input file path, or '-' / omitted for stdin")
    p.add_argument("--out", help="output file path (default: stdout)")
    p.add_argument("--delimiter", default=",",
                   help="CSV delimiter, single character (default: ',')")
    p.add_argument("--version", action="version", version=f"datakonv {__version__}")
    return p


def _read_input(path):
    """Read raw input bytes and decode as UTF-8 (SWR-D02, SWR-D14)."""
    if path == "-":
        stream = sys.stdin
        raw = stream.buffer.read() if hasattr(stream, "buffer") else \
            stream.read().encode("utf-8")
    else:
        try:
            raw = open(path, "rb").read()
        except OSError as e:
            raise DataError(f"cannot read input: {e}")
    try:
        # utf-8-sig: strips a leading BOM (Excel exports) — T-0053, SWR-D14.
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise DataError(f"input is not valid UTF-8: {e}")


def _write_output(text, out_path):
    """Write UTF-8 output to file or stdout (SWR-D02, SWR-D14)."""
    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8", newline="") as f:
                f.write(text)
        except OSError as e:
            raise DataError(f"cannot write output: {e}")
    else:
        if hasattr(sys.stdout, "buffer"):
            sys.stdout.buffer.write(text.encode("utf-8"))
        else:
            sys.stdout.write(text)


def _run(argv):
    args = _parser().parse_args(argv)
    if len(args.delimiter) != 1:
        raise UsageError(f"--delimiter must be a single character, "
                         f"got {args.delimiter!r}")
    text = _read_input(args.input)
    result = csv_to_json(text, args.delimiter) if args.target == "json" \
        else json_to_csv(text, args.delimiter)
    _write_output(result, args.out)
    return EXIT_OK


def main(argv=None):
    """Entry point returning an exit code per SWR-D15 (mapping point, ADR-D03)."""
    try:
        return _run(argv)
    except UsageError as e:
        print(f"datakonv: usage error: {e}", file=sys.stderr)
        return EXIT_USAGE
    except DataError as e:
        print(f"datakonv: data error: {e}", file=sys.stderr)
        return EXIT_DATA
    except SystemExit as e:  # argparse: --help/--version (0), usage error (2)
        return int(e.code or 0)
    except Exception as e:  # unexpected — never crash without a defined code
        print(f"datakonv: internal error: {e}", file=sys.stderr)
        return EXIT_INTERNAL
