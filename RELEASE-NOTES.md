# datakonv 1.0.0 — Release Notes (2026-08-06)

First release of the practice product (project P0 "Genesis", SPL.2, gate G3).

## Features

CSV→JSON (array of objects, automatic typing: number/boolean/null/string, RFC-4180 parsing) and JSON→CSV (flat object arrays, key-union header, RFC-4180 quoting). Files and stdin/stdout, configurable delimiter, `--indent 0–8` for JSON output (0 = compact; added on user feedback T-0059/T-0060), UTF-8 with BOM tolerance on input (problem fix T-0053), defined exit codes 0/1/2/3 with diagnostics on stderr only. Python 3.11+ stdlib, no dependencies.

## Requirements baseline

`req-v1.1`: STK-D01–D05, SWR-D01–D18 (all reviewed). Changes since `req-v1.0`: SWR-D14 precision (BOM), SWR-D18 added (--indent).

## Verification

81 platform-independent checks in total for this product: 42 unit/E2E tests green (unit level SWE.4 + integration/system level SWE.5/6), SWR↔test matrix 18/18 covered, 0 gaps. One real problem cycle (T-0053) and one real change request (T-0060) completed during hardening.

## Known limitations

Flat structures only (nested JSON rejected by design, G1 scope); full in-memory conversion (no streaming, ADR-D02); UTF-8 only.

## Install / run

`pip install .` provides the `datakonv` console command; without install: `python -m datakonv` (PYTHONPATH=src).
