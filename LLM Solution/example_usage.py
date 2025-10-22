"""
Beispiel: Verwendung des LLM Sentiment Analyzers
Zeigt verschiedene Use Cases und Modi
"""

import sys
from pathlib import Path

# Füge aktuelles Verzeichnis zum Python Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from llm_sentiment_analyzer import LLMSentimentAnalyzer


def example_1_basic_usage():
    """Beispiel 1: Basis-Verwendung"""
    print("\n" + "="*70)
    print("BEISPIEL 1: Basis-Verwendung")
    print("="*70)

    # Initialisiere Analyzer (Lexikon-Modus für schnelle Demo)
    analyzer = LLMSentimentAnalyzer(use_bert=False)

    # Analysiere einen Text
    text = "This is an excellent article! Very helpful and informative."
    result = analyzer.analyze(text)

    print(f"\nText: {text}")
    print(f"Score: {result['score']:+.3f}")
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Method: {result['method']}")


def example_2_multilingual():
    """Beispiel 2: Multi-Language Support"""
    print("\n" + "="*70)
    print("BEISPIEL 2: Multi-Language Support")
    print("="*70)

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    texts = [
        ("English", "This article is excellent and very helpful!"),
        ("Deutsch", "Dieser Artikel ist hervorragend und sehr hilfreich!"),
        ("Français", "Cet article est excellent et très utile!"),
        ("Italiano", "Questo articolo è eccellente e molto utile!"),
    ]

    for language, text in texts:
        result = analyzer.analyze(text)
        print(f"\n[{language}] {text}")
        print(f"  → Score: {result['score']:+.3f}, Category: {result['category']}")


def example_3_intranet_comments():
    """Beispiel 3: Intranet-Kommentare analysieren"""
    print("\n" + "="*70)
    print("BEISPIEL 3: Intranet-Kommentare analysieren")
    print("="*70)

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    # Simulierte Kommentare zu einem Intranet-Artikel
    article_url = "https://intranet.company.com/article/123"
    comments = [
        "Great overview of the new policy! Very clear and helpful.",
        "Thanks for sharing, this clarifies a lot of questions.",
        "I found this confusing and not very useful.",
        "Perfect timing, exactly what I needed!",
        "Unfortunately, some important details are missing.",
        "Good article, but could be more detailed.",
    ]

    print(f"\nArtikel: {article_url}")
    print(f"Anzahl Kommentare: {len(comments)}")
    print("\nKommentar-Analyse:")

    for i, comment in enumerate(comments, 1):
        result = analyzer.analyze(comment)
        sentiment_icon = "😊" if result['score'] > 0 else "😐" if result['score'] == 0 else "😞"

        print(f"\n  {i}. {sentiment_icon} {comment}")
        print(f"     Score: {result['score']:+.3f}, Kategorie: {result['category']}")

    # Aggregierte Statistik
    aggregate = analyzer.get_aggregate_sentiment(comments)
    print(f"\n{'─'*70}")
    print(f"AGGREGIERTE STATISTIK:")
    print(f"  Durchschnittlicher Score: {aggregate['avg_score']:+.3f}")
    print(f"  Positive Kommentare: {aggregate['positive_ratio']:.1%}")
    print(f"  Negative Kommentare: {aggregate['negative_ratio']:.1%}")
    print(f"  Neutrale Kommentare: {aggregate['neutral_ratio']:.1%}")

    # Empfehlung basierend auf Sentiment
    if aggregate['avg_score'] > 0.3:
        recommendation = "✓ Artikel kommt sehr gut an!"
    elif aggregate['avg_score'] < -0.3:
        recommendation = "⚠ Artikel braucht Überarbeitung"
    else:
        recommendation = "→ Artikel ist okay, könnte verbessert werden"

    print(f"\n  Empfehlung: {recommendation}")


def example_4_compare_modes():
    """Beispiel 4: Vergleich BERT vs. Lexikon"""
    print("\n" + "="*70)
    print("BEISPIEL 4: Vergleich BERT vs. Lexikon Mode")
    print("="*70)

    test_texts = [
        "This is a great article, very helpful!",
        "Not good, confusing and unclear.",
        "Average content, nothing special.",
    ]

    print("\nLexikon Mode:")
    analyzer_lexicon = LLMSentimentAnalyzer(use_bert=False)
    for text in test_texts:
        result = analyzer_lexicon.analyze(text)
        print(f"  {text}")
        print(f"    → {result['score']:+.3f} ({result['category']})")

    print("\nBERT Mode:")
    analyzer_bert = LLMSentimentAnalyzer(use_bert=True)
    for text in test_texts:
        result = analyzer_bert.analyze(text)
        print(f"  {text}")
        print(f"    → {result['score']:+.3f} ({result['category']})")

    print("\nHinweis: BERT Model verwendet zufällige Gewichte (nicht trainiert).")
    print("         Für Produktion würden trainierte Gewichte verwendet.")


def example_5_batch_processing():
    """Beispiel 5: Batch-Verarbeitung"""
    print("\n" + "="*70)
    print("BEISPIEL 5: Batch-Verarbeitung")
    print("="*70)

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    # Simuliere viele Kommentare
    comments = [
        "Excellent article!",
        "Very helpful, thanks!",
        "Great overview.",
        "Not clear.",
        "Confusing content.",
        "Good explanation.",
        "Perfect!",
        "Could be better.",
    ] * 3  # 24 Kommentare

    print(f"\nVerarbeite {len(comments)} Kommentare...")

    # Batch-Analyse
    results = analyzer.analyze_batch(comments)

    # Zähle Kategorien
    positive = sum(1 for r in results if r['category'] == 'positive')
    negative = sum(1 for r in results if r['category'] == 'negative')
    neutral = sum(1 for r in results if r['category'] == 'neutral')

    print(f"\nErgebnisse:")
    print(f"  Positive: {positive} ({positive/len(comments):.1%})")
    print(f"  Negative: {negative} ({negative/len(comments):.1%})")
    print(f"  Neutral: {neutral} ({neutral/len(comments):.1%})")


def example_6_edge_cases():
    """Beispiel 6: Edge Cases und Negationen"""
    print("\n" + "="*70)
    print("BEISPIEL 6: Edge Cases und Negationen")
    print("="*70)

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    edge_cases = [
        "This is not bad.",  # Negation + negatives Wort = positiv
        "This is not good.",  # Negation + positives Wort = negativ
        "Very very good!",  # Verstärker
        "Extremely terrible.",  # Verstärker + negativ
        "",  # Leerer String
        "123 456",  # Nur Zahlen
    ]

    print("\nSpezialfälle:")
    for text in edge_cases:
        result = analyzer.analyze(text)
        display_text = text if text else "(empty)"
        print(f"\n  '{display_text}'")
        print(f"    → Score: {result['score']:+.3f}, Kategorie: {result['category']}")


def main():
    """Hauptfunktion - führt alle Beispiele aus"""
    print("\n" + "="*70)
    print("  LLM SENTIMENT ANALYZER - BEISPIEL-VERWENDUNG")
    print("="*70)

    examples = [
        example_1_basic_usage,
        example_2_multilingual,
        example_3_intranet_comments,
        example_4_compare_modes,
        example_5_batch_processing,
        example_6_edge_cases,
    ]

    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Fehler in {example_func.__name__}: {e}")

    print("\n" + "="*70)
    print("  FERTIG!")
    print("="*70)
    print("\nWeitere Informationen: Siehe README.md")
    print()


if __name__ == "__main__":
    main()
