# Stakeholder Requirements — datakonv (v1, Sprint 4, T-0043)

*Stakeholder: the client (E. John), who commissioned the practice product (D016) and answered the RM clarifications (2026-08-06: array of objects; strict nesting error; automatic typing; files + stdin/stdout). Language: English (D011).*

| ID | Title | Requirement | Source | Prio | Status |
|---|---|---|---|---|---|
| STK-D01 | CSV/JSON conversion tool | The product shall be a command-line tool that converts CSV to JSON and JSON to CSV, runnable as a single Python 3.11+ stdlib-only package (no third-party dependencies). | D016, P0 ch. 5 | high | reviewed |
| STK-D02 | Defined formats | Supported formats shall be precisely defined: RFC-4180-style CSV (configurable delimiter, quoting, UTF-8) and JSON arrays of flat objects; the mapping between them shall be documented and deterministic. | D016, clarifications | high | reviewed |
| STK-D03 | Defined error behavior | Invalid or unsupported input (malformed CSV/JSON, inconsistent columns, nested JSON values) shall produce clear diagnostics and documented exit codes so the tool is safely scriptable. | D016, clarifications | high | reviewed |
| STK-D04 | Pipeline usability | The tool shall work both on files and in shell pipelines (stdin/stdout), following common CLI conventions (`--help`, `--version`, errors on stderr). | clarifications | medium | reviewed |
| STK-D05 | Verified quality | Every software requirement shall be covered by automated unit verification running in CI on every push, with full SWR↔test traceability. | P0 ch. 5 (SWE.4), T-0026 | high | reviewed |
