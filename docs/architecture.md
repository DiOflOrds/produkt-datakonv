# Architecture — datakonv (SWE.2, Sprint 4, T-0044)

*Baseline input: requirements `req-v1.0` (G1/D018). Language: English (D011, engineering artifact); the human-facing G2 template is German. ADRs in `adr/`.*

## Overview

`datakonv` is a stdlib-only Python package under `src/datakonv/`, invoked as `python -m datakonv`. Data flow: CLI parses arguments and resolves input/output streams → conversion unit (C2J or J2C) transforms fully in memory → CLI writes the result. All error signalling uses two exception types mapped centrally to exit codes.

## Units and interfaces

| Unit | Module | Responsibility | SWRs |
|---|---|---|---|
| CLI | `src/datakonv/cli.py` (+ `__main__.py`) | Argument parsing (`--to`, `--out`, `--delimiter`, `--help`, `--version`), stream resolution (file/stdin/stdout, UTF-8), central exception→exit-code mapping, diagnostics to stderr. `main(argv) -> int`. | SWR-D01–D04, D14, D15 |
| C2J | `src/datakonv/c2j.py` | `csv_to_json(text: str, delimiter: str) -> str`. Header handling, RFC-4180 parsing (stdlib `csv`), record validation (field count, duplicate/empty headers), deterministic typing (number/bool/null/string). | SWR-D05–D09, D16, D17 |
| J2C | `src/datakonv/j2c.py` | `json_to_csv(text: str, delimiter: str) -> str`. Parse + structure validation (array of flat objects), key-union header in first-occurrence order, value serialization with RFC-4180 quoting, JSON-path error reporting. | SWR-D10–D13, D16, D17 |
| Errors | `src/datakonv/errors.py` | `UsageError` (exit 2), `DataError` (exit 3), exit-code constants. No logic. | SWR-D15 |

Interface contract: conversion units are pure functions `str -> str` — no I/O, no process exit, no global state. Only the CLI touches streams and exit codes. This keeps units independently testable and the determinism requirements (SWR-D16/D17) verifiable at function level.

## Traceability SWR ↔ unit

All 17 SWRs map to exactly one owning unit (table above); SWR-D16/D17 (determinism, round-trip) are cross-cutting properties verified over C2J+J2C. No SWR is unassigned; no unit exists without SWRs.

## Decisions (ADRs)

- **ADR-D01** — stdlib-only, src-layout, `python -m` entry point (packaging deferred to release, Sprint 5).
- **ADR-D02** — full in-memory conversion, no streaming (scope guard from G1; revisit only via CR).
- **ADR-D03** — exception-based error model with central exit-code mapping in the CLI (single enforcement point for SWR-D15).
