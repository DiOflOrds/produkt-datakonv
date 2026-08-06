# ADR-D02: Vollständige In-Memory-Konvertierung (kein Streaming)

*Status: entschieden (ARCH, 2026-08-06, T-0044). Gate: G2-Vorlage.*

## Kontext

J2C braucht die Schlüssel-Union ALLER Objekte für den Header (SWR-D11) — echtes Streaming erforderte zwei Durchläufe oder Header-Nachtrag. G1 hat Streaming großer Dateien explizit aus dem Schnitt genommen.

## Optionen

1. Streaming/Two-Pass: speicherschonend, aber deutlich mehr Komplexität und Randfälle.
2. **Alles im Speicher (`str -> str`-Funktionen):** einfach, deterministisch (SWR-D16/D17 trivial prüfbar), für die Zielgröße (Übungsprodukt) völlig ausreichend.

## Entscheidung

Option 2. Konvertierungsfunktionen sind reine `str -> str`-Funktionen ohne I/O.

## Konsequenzen

Speicherbedarf ~ Eingabegröße — akzeptiert; Streaming nur per CR mit neuem G1-Schnitt (Wiedervorlage nach P0).
