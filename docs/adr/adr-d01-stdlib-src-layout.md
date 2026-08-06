# ADR-D01: stdlib-only package, src-layout, `python -m` entry

*Status: entschieden (ARCH, 2026-08-06, T-0044). Gate: G2-Vorlage.*

## Kontext

STK-D01/SWR-D16 fordern ein abhängigkeitsfreies, deterministisches CLI-Tool; die Plattform-Lessons (T-0027: CI-Drift durch externe Pakete) gelten auch fürs Produkt.

## Optionen

1. Flat layout + Third-party-CLI-Framework (click): komfortabel, aber externe Abhängigkeit.
2. **src-layout (`src/datakonv/`) + argparse + `python -m datakonv`:** null Abhängigkeiten, saubere Test-Imports, Standard-Konvention.

## Entscheidung

Option 2. `csv`/`json`/`argparse` aus der Standardbibliothek decken alle Anforderungen; Packaging (pyproject, Konsolen-Skript) folgt erst mit dem Release (SPL.2, Sprint 5).

## Konsequenzen

Aufruf bis zum Release nur via `python -m datakonv` bzw. Tests; Tests importieren über `src/`-Pfad.
