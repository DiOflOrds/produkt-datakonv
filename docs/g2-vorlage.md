# G2-Vorlage — Architektur datakonv (Sprint 4, T-0044)

*An den Auftraggeber. Architektur-/Technologie-Freigabe fürs Übungsprodukt (`docs/architecture.md`, ADR-D01–D03).*

## Kern

4 Units — CLI (Argumente, I/O, zentrales Exit-Code-Mapping), C2J (CSV→JSON), J2C (JSON→CSV), Errors. Konvertierung als reine `str -> str`-Funktionen ohne I/O (unabhängig testbar); alles In-Memory (ADR-D02, G1-Schnitt); stdlib-only mit `python -m datakonv` (ADR-D01); Fehlermodell mit genau zwei Exception-Typen und einem Durchsetzungspunkt für Exit-Codes (ADR-D03). Alle 17 SWRs sind genau einer Unit zugeordnet.

## Entscheidung

- **G2a (Empfehlung):** freigeben — Implementierung startet (T-0045)
- **G2b:** mit Auflagen freigeben
- **G2c:** zurückweisen

**Frist:** 2026-08-08 · **Default:** kein Default — blockiert T-0045/T-0046.

---

**Entscheidung (D019, via Session-Dialog, 2026-08-06): G2a — freigegeben.** T-0045/T-0046 entblockt.
