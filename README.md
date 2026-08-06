# datakonv — CSV↔JSON converter (CLI)

Practice product of the ASPICE agent team (project P0 "Genesis", decision D016):
a small command-line data converter, built end-to-end by the team following its
own process (SWE.1–SWE.4 in Sprint 4, SWE.5/SWE.6 + release in Sprint 5).

**Status:** skeleton (Sprint 4, T-0042). Requirements follow requirements-first —
no implementation before the SWR set is reviewed and G1 is granted.

## Structure

| Path | Content | Owner |
|---|---|---|
| `requirements/` | Stakeholder (STK) and software requirements (SWR), English (D011) | RM |
| `docs/` | Architecture, ADRs (SWE.2) | ARCH |
| `src/` | Implementation, Python 3 stdlib only (SWE.3) | DEV |
| `tests/` | Unit verification, runs in CI on every push (SWE.4) | TEST |

## Development

Python 3.11+, standard library only. Run tests: `python -m unittest discover -s tests`

Governance: tickets and decisions live in the `p0` repo (file board, T-0042 ff.);
traceability SWR↔test via docstring IDs (matrix mechanics from T-0026).
