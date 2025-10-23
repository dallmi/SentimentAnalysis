#!/usr/bin/env python3
"""
End-to-End Test: Verfolgt Topic-Labels von mBART bis ins Excel
"""

import sys
import json
import pandas as pd
from pathlib import Path

# Add LLM Solution to path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

from main_bertopic import BERTopicSentimentAnalyzer

print("=" * 80)
print("END-TO-END TEST: Topic-Labels von mBART bis Excel")
print("=" * 80)

# Test mit Mini-Dataset
test_data = [
    {
        "url": "https://example.com/article1",
        "title": "Wealth Management and Private Banking",
        "content": "Our wealth management division focuses on high-net-worth clients. Private banking services include portfolio management and investment advisory.",
        "comments": [
            {"text": "Great service!", "author": "John", "date": "2025-01-01"}
        ]
    },
    {
        "url": "https://example.com/article2",
        "title": "Client Referral Program Success",
        "content": "Our referral program generated USD 923 million in net new money. Client relationships are key to business growth.",
        "comments": [
            {"text": "Impressive results", "author": "Jane", "date": "2025-01-02"}
        ]
    },
    {
        "url": "https://example.com/article3",
        "title": "Digital Banking Transformation",
        "content": "Digital transformation in banking sector. New mobile app for retail banking customers with enhanced security features.",
        "comments": [
            {"text": "Love the new app", "author": "Mike", "date": "2025-01-03"}
        ]
    }
]

# Speichere Test-Daten
test_file = Path(__file__).parent / "test_articles.json"
with open(test_file, 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Test-Daten erstellt: {test_file}")
print(f"  {len(test_data)} Artikel")

# Test MIT abstractive (mBART)
print("\n" + "=" * 80)
print("TEST 1: MIT --abstractive (mBART sollte verwendet werden)")
print("=" * 80)

try:
    analyzer = BERTopicSentimentAnalyzer(use_abstractive=True)

    # Prüfe ob mBART geladen wurde
    if analyzer.use_abstractive and analyzer.abstractive_summarizer:
        print("✓ mBART Summarizer ist geladen")
    else:
        print("❌ mBART Summarizer NICHT geladen!")
        print(f"   use_abstractive: {analyzer.use_abstractive}")
        print(f"   abstractive_summarizer: {analyzer.abstractive_summarizer}")

    output_file = Path(__file__).parent / "test_output_abstractive.xlsx"
    analyzer.analyze(str(test_file), str(output_file))

    print("\n" + "=" * 80)
    print("PRÜFE EXCEL OUTPUT:")
    print("=" * 80)

    # Lese Excel und prüfe Topic-Labels
    df = pd.read_excel(output_file, sheet_name='Articles')

    print(f"\n📊 Articles Sheet:")
    print(f"   Spalten: {list(df.columns)}")
    print(f"\n   Topic-Labels im Excel:")

    for idx, row in df.iterrows():
        title = row['Title'][:50]
        topic = row['Topic']
        print(f"      {idx+1}. {title}... → Topic: '{topic}'")

    # Prüfe ob es mBART Labels oder BERTopic Keywords sind
    print("\n" + "=" * 80)
    print("VALIDIERUNG:")
    print("=" * 80)

    has_stopwords = False
    for idx, row in df.iterrows():
        topic = str(row['Topic']).lower()
        if any(sw in topic for sw in ['_the_', '_and_', '_to_', '_of_']):
            print(f"   ❌ Row {idx+1}: Enthält Stoppwörter: '{row['Topic']}'")
            has_stopwords = True

    if has_stopwords:
        print("\n❌ FEHLER: Excel enthält BERTopic Keywords statt mBART Labels!")
        print("   mBART wurde NICHT verwendet für Topic-Labels!")
    else:
        print("\n✓ SUCCESS: Keine Stoppwörter gefunden - sieht nach mBART Labels aus!")

    # Prüfe Summaries
    print(f"\n📝 Summary-Längen:")
    for idx, row in df.iterrows():
        summary_len = len(str(row['Summary']))
        print(f"      {idx+1}. {summary_len} Zeichen")
        if summary_len < 100:
            print(f"         ⚠️  Sehr kurz (< 100 Zeichen)")

except Exception as e:
    print(f"\n❌ FEHLER: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
print("\n" + "=" * 80)
print("CLEANUP:")
print("=" * 80)
print(f"Test-Files:")
print(f"  Input:  {test_file}")
print(f"  Output: {output_file}")
print("\nDu kannst das Excel öffnen und die Topic-Labels manuell prüfen!")
