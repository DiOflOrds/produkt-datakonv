"""J2C unit: JSON -> CSV conversion (pure str -> str, ADR-D02).

SWR reference: SWR-D10 (parse vs structure error), SWR-D11 (key union header,
first-occurrence order, empty for missing), SWR-D12 (value serialization,
RFC-4180 quoting), SWR-D13 (nested values rejected with JSON path).
"""
import csv
import io
import json

from .errors import DataError


def _serialize(value):
    """Scalar serialization per SWR-D12 (nested values handled by caller)."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    return value


def json_to_csv(text, delimiter=","):
    """Convert a JSON array-of-objects string to CSV text (SWR-D10..D13)."""
    try:
        data = json.loads(text)
    except ValueError as e:
        raise DataError(f"JSON parse error: {e}")
    if not isinstance(data, list):
        raise DataError("JSON structure error: top level must be an array of objects")
    header = []
    for i, obj in enumerate(data):
        if not isinstance(obj, dict):
            raise DataError(f"JSON structure error: element [{i}] is not an object")
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                raise DataError(f"nested value not supported at [{i}].{key} "
                                f"(strict mode, G1 scope)")
            if key not in header:
                header.append(key)
    if not data:
        return ""
    out = io.StringIO()
    writer = csv.writer(out, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL,
                        lineterminator="\n")
    writer.writerow(header)
    for obj in data:
        writer.writerow([_serialize(obj.get(k)) for k in header])
    return out.getvalue()
