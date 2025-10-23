#!/usr/bin/env python3
"""
Debug: Testet ob mBART Topic-Label-Generation wirklich funktioniert
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "LLM Solution"))

from abstractive_summarizer import AbstractiveSummarizer

print("=" * 80)
print("DEBUG: mBART Topic-Label-Generation")
print("=" * 80)

# Simuliere BERTopic Keywords
topic_keywords = [
    ('referral', 0.85),
    ('wealth', 0.72),
    ('management', 0.68),
    ('client', 0.55),
    ('business', 0.48),
    ('growth', 0.42),
    ('banking', 0.38),
    ('private', 0.35),
    ('markets', 0.30),
    ('relationship', 0.28)
]

# Representative documents
representative_docs = [
    "How one referral translated to USD 923 million in Net New Money. Referrals can help us grow our business.",
    "Singapore shows. Pleased with our relationship, one of our clients in Banking Espresso: private markets explained.",
    "Banking Espresso: Investmentthemen anhand von Videos unseres Chief Investment Office."
]

print("\n📊 INPUT für mBART:")
print("\nTop 10 Keywords:")
for word, score in topic_keywords[:10]:
    print(f"   - {word}: {score:.2f}")

print("\nRepräsentative Dokumente:")
for i, doc in enumerate(representative_docs, 1):
    print(f"   {i}. {doc[:80]}...")

# Lade mBART
print("\n" + "=" * 80)
print("Lade mBART Model...")
print("=" * 80)

try:
    summarizer = AbstractiveSummarizer()
    print("✓ mBART geladen")

    # Generiere Topic-Label
    print("\n" + "=" * 80)
    print("Generiere Topic-Label...")
    print("=" * 80)

    label = summarizer.generate_topic_label(
        keywords=topic_keywords,
        representative_docs=representative_docs,
        source_lang="de_DE",
        max_keywords=3
    )

    print(f"\n✨ GENERIERTES TOPIC-LABEL:")
    print(f"   \"{label}\"")

    # Prüfe ob es sinnvoll ist
    print("\n" + "=" * 80)
    print("VALIDIERUNG:")
    print("=" * 80)

    if len(label) == 0:
        print("❌ FEHLER: Label ist leer!")
    elif any(stopword in label.lower() for stopword in ['the', 'and', 'to', 'of']):
        print("❌ FEHLER: Enthält Stoppwörter!")
    elif len(label.split()) > 5:
        print("⚠️  WARNING: Label ist zu lang (>5 Wörter)")
    else:
        print("✓ Label sieht gut aus!")

    print(f"\nErwartet: 1-3 prägnante Schlagwörter")
    print(f"Erhalten: {len(label.split())} Wörter")

except Exception as e:
    print(f"\n❌ FEHLER: {e}")
    import traceback
    traceback.print_exc()
