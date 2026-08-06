# Software Requirements — datakonv (v1.1, Sprint 5: SWR-D14 precision T-0053, SWR-D18 added T-0060; v1 Sprint 4, T-0043)

*Derived from `../stakeholder/stakeholder-requirements.md`. Components: CLI = argument handling and I/O wiring, C2J = CSV→JSON conversion, J2C = JSON→CSV conversion, GEN = cross-cutting. Language: English (D011). Status `reviewed` = reviewed for feasibility (ARCH/DEV context) and verifiability (QM/TEST context) per DoD checklist; implementation follows requirements-first (T-0025).*

## Command-line interface (CLI)

| ID | Requirement | Trace | Verification | Prio | Status |
|---|---|---|---|---|---|
| SWR-D01 | The CLI shall require a direction option `--to json` or `--to csv`; a missing or invalid value shall produce a usage error (exit 2) with a usage message on stderr. | STK-D01, STK-D03 | Unit tests `test_cli.py` (direction cases) | high | reviewed |
| SWR-D02 | The CLI shall read input from a file path argument, or from stdin when the path is `-` or omitted; it shall write output to the file given by `--out <path>`, or to stdout when `--out` is omitted. | STK-D04 | Unit tests (file/stdin × file/stdout matrix) | high | reviewed |
| SWR-D03 | The CLI shall accept `--delimiter <char>` (single character, default `,`) applied to CSV input and CSV output; a multi-character value shall produce a usage error (exit 2). | STK-D02 | Unit tests (delimiter variants, invalid value) | medium | reviewed |
| SWR-D04 | The CLI shall support `--help` and `--version`, each exiting 0 after printing to stdout. | STK-D04 | Unit tests (flags) | low | reviewed |
| SWR-D18 | The CLI shall accept `--indent <n>` (integer 0–8, default 2) for JSON output: n ≥ 1 produces pretty-printed output with n spaces, 0 produces compact single-line output; other values produce a usage error (exit 2). (CR T-0060 from human feedback T-0059, v1.1) | STK-D04 | Unit tests (indent variants, invalid values) + E2E | medium | reviewed |

## CSV → JSON (C2J)

| ID | Requirement | Trace | Verification | Prio | Status |
|---|---|---|---|---|---|
| SWR-D05 | C2J shall treat the first CSV record as the header and produce a JSON array of objects whose keys are the header names in column order, one object per data record. | STK-D02 | Unit tests `test_c2j.py` (shape, key order) | high | reviewed |
| SWR-D06 | C2J shall type values deterministically: fields matching the JSON number grammar become numbers, `true`/`false` (case-insensitive) become booleans, empty fields become `null`, all other fields become strings. | STK-D02 | Unit tests (typing table incl. edge cases `01`, `1e3`, `True`) | high | reviewed |
| SWR-D07 | C2J shall parse quoted CSV fields per RFC 4180, including embedded delimiters, escaped quotes (`""`), and embedded line breaks. | STK-D02 | Unit tests (quoting cases) | high | reviewed |
| SWR-D08 | C2J shall reject a data record whose field count differs from the header with a data error (exit 3) naming the record number on stderr. | STK-D03 | Unit tests (short/long record) | high | reviewed |
| SWR-D09 | C2J shall reject input with duplicate or empty header names with a data error (exit 3) naming the offending column. | STK-D03 | Unit tests (duplicate/empty header) | medium | reviewed |

## JSON → CSV (J2C)

| ID | Requirement | Trace | Verification | Prio | Status |
|---|---|---|---|---|---|
| SWR-D10 | J2C shall accept only a JSON array of objects; syntactically invalid JSON or any other top-level structure shall produce a data error (exit 3) distinguishing parse error from structure error on stderr. | STK-D03 | Unit tests `test_j2c.py` (parse vs structure) | high | reviewed |
| SWR-D11 | J2C shall output a header containing the union of all object keys in first-occurrence order, one CSV record per object, writing empty fields for keys absent in an object. | STK-D02 | Unit tests (key union, order, missing keys) | high | reviewed |
| SWR-D12 | J2C shall serialize values as: strings verbatim, numbers and booleans as their JSON literal text, `null` as empty field — applying RFC-4180 quoting whenever a field contains delimiter, quote, or line break. | STK-D02 | Unit tests (serialization table, quoting) | high | reviewed |
| SWR-D13 | J2C shall reject any object value that is itself an object or array with a data error (exit 3) naming the JSON path (e.g. `[2].address`) on stderr. | STK-D03 | Unit tests (nested object/array, path in message) | high | reviewed |

## Cross-cutting (GEN)

| ID | Requirement | Trace | Verification | Prio | Status |
|---|---|---|---|---|---|
| SWR-D14 | All input and output shall be UTF-8; a leading UTF-8 BOM on input shall be accepted and stripped (precision v1.1, problem T-0053); output shall never start with a BOM; input that is not valid UTF-8 shall produce a data error (exit 3). | STK-D02, STK-D03 | Unit tests (umlauts, invalid bytes, BOM strip) + E2E `test_e2e.py` | medium | reviewed |
| SWR-D15 | Exit codes shall be exactly: 0 success, 2 usage error, 3 data/format error, 1 unexpected internal error; all diagnostics shall go to stderr and never to stdout. | STK-D03, STK-D04 | Unit tests (exit-code matrix, stream separation) | high | reviewed |
| SWR-D16 | Identical input and options shall produce byte-identical output (deterministic conversion, stable ordering, no timestamps). | STK-D02, STK-D05 | Unit test (double-run comparison) | medium | reviewed |
| SWR-D17 | A full round-trip CSV→JSON→CSV over typed flat data shall reproduce the original CSV byte-identically (given default options and normalized quoting). | STK-D02, STK-D05 | Unit test (round-trip property) | medium | reviewed |

## Traceability summary

| STK | covered by |
|---|---|
| STK-D01 | SWR-D01 |
| STK-D02 | SWR-D03, SWR-D05, SWR-D06, SWR-D07, SWR-D11, SWR-D12, SWR-D14, SWR-D16, SWR-D17 |
| STK-D03 | SWR-D01, SWR-D08, SWR-D09, SWR-D10, SWR-D13, SWR-D14, SWR-D15 |
| STK-D04 | SWR-D02, SWR-D04, SWR-D15, SWR-D18 |
| STK-D05 | SWR-D16, SWR-D17 (+ CI gate T-0042, matrix T-0046) |

*18 SWRs (v1.1), all STKs covered, no orphan SWRs. DoD checklist (`process/checklists/dod-sw-anforderung.md`) applied per SWR on 2026-08-06: atomic, testable, traced, verification named — QM/ARCH review contexts documented in T-0043.*
