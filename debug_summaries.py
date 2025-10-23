#!/usr/bin/env python3
"""
Debug Script: Überprüft ob Abstractive Summarization wirklich funktioniert
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

from abstractive_summarizer import AbstractiveSummarizer

# Langer deutscher Corporate-Text (>1000 Zeichen)
long_article = """
Die Geschäftsführung der Example AG hat am Montag umfassende neue Regelungen für Homeoffice
und flexible Arbeitszeiten angekündigt. Nach mehrmonatigen Verhandlungen mit dem Betriebsrat
wurde eine Einigung erzielt, die ab dem 1. Februar 2025 in Kraft tritt.

Mitarbeiter können künftig bis zu drei Tage pro Woche von zu Hause arbeiten. Die neue Regelung
gilt für alle Vollzeitbeschäftigten, die seit mindestens sechs Monaten im Unternehmen tätig sind.
Teilzeitbeschäftigte erhalten anteilig entsprechende Homeoffice-Tage.

Der Vorstand betonte, dass diese Maßnahme die Work-Life-Balance der Mitarbeiter verbessern und
gleichzeitig die Produktivität steigern soll. Eine Evaluierung der neuen Regelung ist nach sechs
Monaten geplant. Zusätzlich werden flexible Kernarbeitszeiten zwischen 10 und 15 Uhr eingeführt.

Die IT-Abteilung stellt die notwendige Hardware und Software zur Verfügung. Für die Nutzung ist
ein Antrag über das HR-Portal erforderlich. Führungskräfte müssen die Anträge innerhalb von fünf
Arbeitstagen prüfen. Bei Ablehnung muss eine schriftliche Begründung erfolgen.

Die neue Regelung gilt für alle Abteilungen außer dem Kundenservice. Mitarbeiter im Kundenservice
haben spezielle Schichtpläne und sind davon ausgenommen. Für sie werden separate Lösungen erarbeitet.
"""

print("=" * 80)
print("DEBUG: Abstractive vs Extractive Summarization")
print("=" * 80)

print(f"\n📄 ORIGINAL ARTIKEL:")
print(f"   Länge: {len(long_article)} Zeichen / {len(long_article.split())} Wörter")
print(f"\n{long_article[:500]}...")

# Test 1: Abstractive mit max_length=100 (ALT - zu kurz!)
print("\n" + "=" * 80)
print("TEST 1: Abstractive mit max_length=100 (ALT)")
print("=" * 80)

try:
    summarizer = AbstractiveSummarizer()

    summary_100 = summarizer.summarize(
        long_article,
        source_lang="de_DE",
        max_length=100,  # ALT: Nur 100 tokens!
        min_length=30
    )

    print(f"\n✨ Summary (max_length=100):")
    print(f"   Länge: {len(summary_100)} Zeichen / {len(summary_100.split())} Wörter")
    print(f"\n{summary_100}")
    print(f"\n⚠️  Abgeschnitten bei ~{len(summary_100)} Zeichen!")

except Exception as e:
    print(f"❌ Fehler: {e}")

# Test 2: Abstractive mit max_length=200 (NEU - länger!)
print("\n" + "=" * 80)
print("TEST 2: Abstractive mit max_length=200 (NEU)")
print("=" * 80)

try:
    summary_200 = summarizer.summarize(
        long_article,
        source_lang="de_DE",
        max_length=200,  # NEU: 200 tokens!
        min_length=50
    )

    print(f"\n✨ Summary (max_length=200):")
    print(f"   Länge: {len(summary_200)} Zeichen / {len(summary_200.split())} Wörter")
    print(f"\n{summary_200}")

    if len(summary_200) > len(summary_100):
        print(f"\n✓ Länger als vorher! (+{len(summary_200) - len(summary_100)} Zeichen)")

except Exception as e:
    print(f"❌ Fehler: {e}")

# Vergleich
print("\n" + "=" * 80)
print("VERGLEICH:")
print("=" * 80)
print(f"Original:              {len(long_article)} Zeichen")
print(f"Summary (max_len=100): {len(summary_100)} Zeichen (ALT)")
print(f"Summary (max_len=200): {len(summary_200)} Zeichen (NEU)")
print(f"\nDifferenz: +{len(summary_200) - len(summary_100)} Zeichen")

# Check ob es wirklich abstractive ist
if summary_100[:100] in long_article:
    print("\n⚠️  WARNING: Summary scheint 1:1 Kopie zu sein!")
else:
    print("\n✓ Summary ist neu generiert (nicht 1:1 Kopie)")
