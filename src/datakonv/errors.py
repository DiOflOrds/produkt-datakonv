"""Error model (ADR-D03): two exception types, central exit-code mapping in the CLI.

SWR reference: SWR-D15 (exit codes 0/1/2/3, diagnostics on stderr only).
"""

EXIT_OK = 0
EXIT_INTERNAL = 1
EXIT_USAGE = 2
EXIT_DATA = 3


class UsageError(Exception):
    """Invalid command-line usage (mapped to exit 2)."""


class DataError(Exception):
    """Invalid or unsupported input data (mapped to exit 3)."""
