# G1-Vorlage — Anforderungs-Baseline datakonv (Sprint 4, T-0043)

*An den Auftraggeber. Freigabe der Anforderungs-Baseline für das Übungsprodukt (D016). Nach Freigabe wird `req-v1.0` auf produkt-datakonv getaggt; erst danach beginnt die Implementierung (requirements-first, T-0025).*

## Umfang

**5 Stakeholder-Anforderungen (STK-D01–D05)** und **17 Software-Anforderungen (SWR-D01–D17)**, Englisch (D011), alle im Status reviewed (DoD-Checkliste je SWR bestanden; Machbarkeit im ARCH/DEV-Kontext, Prüfbarkeit im QM/TEST-Kontext).

**Produktschnitt** (aus deinen Clarifications vom 2026-08-06): CLI `datakonv` konvertiert CSV↔JSON — CSV→JSON als Array von Objekten mit automatischer Typisierung (Zahl/Bool/null/String), JSON→CSV nur für flache Objekt-Arrays mit striktem Fehler bei Verschachtelung, Dateien und stdin/stdout, Trennzeichen konfigurierbar, UTF-8, Exit-Codes 0/1/2/3, Python-stdlib ohne Abhängigkeiten.

**Bewusst außerhalb des Schnitts:** Flattening verschachtelter JSON-Strukturen, andere Encodings, Schema-Validierung, Streaming großer Dateien — bei Bedarf als CRs in Sprint 5+.

## Entscheidung

**Frage:** Anforderungs-Baseline datakonv (STK-D01–D05, SWR-D01–D17) freigeben?

- **G1a (Empfehlung):** freigeben — Baseline `req-v1.0`, Implementierung startet (T-0044 ff.)
- **G1b:** mit Auflagen freigeben (Auflagen bitte benennen)
- **G1c:** zurückweisen (Begründung bitte benennen)

**Frist:** 2026-08-08 · **Default:** kein Default — blockiert T-0044–T-0046.

---

**Entscheidung (D018, via Session-Dialog, 2026-08-06): G1a — freigegeben.** Baseline `req-v1.0` getaggt; T-0044–T-0046 entblockt.
