"""C2J unit: CSV -> JSON conversion (pure str -> str, ADR-D02).

SWR reference: SWR-D05 (array of objects, header keys, column order),
SWR-D06 (deterministic typing), SWR-D07 (RFC-4180 parsing),
SWR-D08 (field-count mismatch), SWR-D09 (duplicate/empty header).
"""
import csv
import io
import json
import re

from .errors import DataError

_NUMBER_RE = re.compile(r"^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$")


def _type_value(field):
    """Deterministic typing per SWR-D06: number / boolean / null / string."""
    if field == "":
        return None
    if field.lower() in ("true", "false"):
        return field.lower() == "true"
    if _NUMBER_RE.match(field):
        return float(field) if any(c in field for c in ".eE") else int(field)
    return field


def csv_to_json(text, delimiter=","):
    """Convert CSV text to a JSON array-of-objects string (SWR-D05..D09)."""
    records = list(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter))
    if not records:
        raise DataError("empty input: missing CSV header record")
    header = records[0]
    seen = set()
    for i, name in enumerate(header, start=1):
        if name == "":
            raise DataError(f"empty header name in column {i}")
        if name in seen:
            raise DataError(f"duplicate header name in column {i}: {name!r}")
        seen.add(name)
    objects = []
    for nr, record in enumerate(records[1:], start=2):
        if len(record) != len(header):
            raise DataError(f"record {nr}: {len(record)} field(s), "
                            f"expected {len(header)} (header)")
        objects.append({k: _type_value(v) for k, v in zip(header, record)})
    return json.dumps(objects, ensure_ascii=False, indent=2) + "\n"
