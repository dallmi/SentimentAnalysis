#!/usr/bin/env python3
"""
Analysiert den Code-Flow für Topic-Labels von mBART bis Excel
Zeigt wo die Labels gesetzt, überschrieben oder verwendet werden
"""

import re
from pathlib import Path

print("=" * 80)
print("CODE-FLOW ANALYSE: Topic-Labels von mBART → Excel")
print("=" * 80)

main_file = Path(__file__).parent / "main_bertopic.py"
content = main_file.read_text(encoding='utf-8')

print("\n📝 Analysiere main_bertopic.py...\n")

# Suche alle Stellen wo topic_labels gesetzt oder verwendet wird
patterns = {
    "topic_labels initialisiert": r"topic_labels\s*=\s*\{\}",
    "topic_labels[topic_id] = ...": r"topic_labels\[topic_id\]\s*=",
    "articles_df['topic_label'] = ...": r"articles_df\['topic_label'\]\s*=",
    "Excel: overview_df = ...": r"overview_df\s*=\s*articles_df\[\[.*'topic_label'",
    "Excel: columns renamed": r"overview_df\.columns\s*=",
}

findings = {}
for description, pattern in patterns.items():
    matches = []
    for i, line in enumerate(content.split('\n'), 1):
        if re.search(pattern, line):
            matches.append((i, line.strip()))
    findings[description] = matches

print("🔍 GEFUNDENE CODE-STELLEN:\n")

for description, matches in findings.items():
    print(f"   {description}:")
    if matches:
        for line_num, line_content in matches:
            print(f"      Zeile {line_num}: {line_content[:80]}")
    else:
        print(f"      ❌ NICHT GEFUNDEN!")
    print()

# Spezifische Analyse
print("=" * 80)
print("DETAILLIERTE ANALYSE:")
print("=" * 80)

# Check: Wird topic_labels Dictionary nach mBART-Generation überschrieben?
lines = content.split('\n')
topic_labels_init_line = None
topic_labels_used_line = None

for i, line in enumerate(lines):
    if 'topic_labels = {}' in line:
        topic_labels_init_line = i + 1
    if "articles_df['topic_label'] = articles_df['topic'].map(topic_labels)" in line:
        topic_labels_used_line = i + 1

print(f"\n1. topic_labels Dictionary:")
print(f"   Initialisiert: Zeile {topic_labels_init_line}")
print(f"   Verwendet für DataFrame: Zeile {topic_labels_used_line}")

if topic_labels_init_line and topic_labels_used_line:
    lines_between = topic_labels_used_line - topic_labels_init_line
    print(f"   → {lines_between} Zeilen Code dazwischen")

    # Check ob es mehrere Initialisierungen gibt
    init_count = content.count('topic_labels = {}')
    if init_count > 1:
        print(f"   ⚠️  WARNING: topic_labels wird {init_count}x initialisiert!")
    else:
        print(f"   ✓ topic_labels wird nur 1x initialisiert")

# Check Excel-Ausgabe
print(f"\n2. Excel-Ausgabe:")
excel_patterns = [
    ("DataFrame Erstellung", r"overview_df\s*=\s*articles_df\[\["),
    ("Spalten-Umbenennung", r"overview_df\.columns\s*="),
    ("Excel Writer", r"overview_df\.to_excel"),
]

for desc, pat in excel_patterns:
    match = re.search(pat, content)
    if match:
        # Finde Zeilennummer
        line_num = content[:match.start()].count('\n') + 1
        print(f"   {desc}: Zeile {line_num}")
    else:
        print(f"   {desc}: ❌ NICHT GEFUNDEN")

print("\n" + "=" * 80)
print("POTENZIELLE PROBLEME:")
print("=" * 80)

issues = []

# Check 1: Wird topic_label korrekt aus DataFrame gelesen?
if "'topic_label'" in content:
    print("✓ 'topic_label' Spalte existiert im Code")
else:
    issues.append("❌ 'topic_label' Spalte nicht gefunden")

# Check 2: Reihenfolge der Spalten
if "['url', 'title', 'summary', 'topic_label', 'topic']" in content:
    print("✓ Spalten-Reihenfolge korrekt: ..., 'topic_label', 'topic'")
else:
    issues.append("⚠️  Spalten-Reihenfolge könnte falsch sein")

# Check 3: Spalten-Umbenennung
if "['URL', 'Title', 'Summary', 'Topic', 'Topic_ID']" in content:
    print("✓ Spalten-Umbenennung: topic_label → Topic, topic → Topic_ID")
else:
    issues.append("⚠️  Spalten-Umbenennung nicht standard")

if not issues:
    print("\n✓ Keine offensichtlichen Code-Probleme gefunden")
else:
    print("\nGefundene Issues:")
    for issue in issues:
        print(f"   {issue}")

print("\n" + "=" * 80)
print("EMPFEHLUNG:")
print("=" * 80)
print("""
Der Code sieht strukturell korrekt aus. Das Problem könnte sein:

1. mBART Labels werden generiert aber von BERTopic Standard-Namen überschrieben
2. Die Reihenfolge der Code-Ausführung ist falsch
3. topic_labels Dictionary wird irgendwo geleert oder zurückgesetzt

LÖSUNG: Füge Debug-Output hinzu DIREKT vor Excel-Schreibvorgang:
   - Zeige topic_labels Dictionary
   - Zeige articles_df['topic_label'].head()

Das wurde bereits implementiert mit der "🔍 DEBUG" Sektion.

NÄCHSTER SCHRITT:
Führe die Analysis auf Windows mit --abstractive aus und schau dir an:
   - 🔍 DEBUG: topic_labels Dictionary: Was steht hier?
   - ✨ Finale Topic-Labels (mBART): Was steht hier?

Wenn beide zeigen "0_the_and_to_of" statt "Banking & Finance",
dann wird mBART nie aufgerufen!
""")
