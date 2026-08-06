# ADR-D03: Exception-basiertes Fehlermodell mit zentralem Exit-Code-Mapping

*Status: entschieden (ARCH, 2026-08-06, T-0044). Gate: G2-Vorlage.*

## Kontext

SWR-D15 verlangt exakt vier Exit-Codes und strikte stdout/stderr-Trennung; Fehlerfälle entstehen in drei Units (CLI, C2J, J2C).

## Optionen

1. Jede Unit ruft selbst `sys.exit()`: verstreute Exit-Punkte, Units nicht rein testbar.
2. **Zwei Exception-Typen (`UsageError`→2, `DataError`→3), Mapping ausschließlich in `cli.main`; unerwartete Exceptions → 1:** ein Durchsetzungspunkt, Units bleiben reine Funktionen.

## Entscheidung

Option 2. `cli.main(argv) -> int` fängt beide Typen, schreibt die Meldung nach stderr und liefert den Code; `__main__` ruft nur `sys.exit(main())`.

## Konsequenzen

SWR-D15 ist an genau einer Stelle testbar; Konvertierungs-Units kennen weder Streams noch Exit-Codes (ADR-D02-konform).
