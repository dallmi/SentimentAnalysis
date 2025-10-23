"""
Test-Script für Sentiment Analysis Module

Testet alle Komponenten mit Beispieldaten
"""

import sys
from pathlib import Path

# Test 1: Sentiment Model
print("=" * 60)
print("TEST 1: Lightweight Sentiment Model")
print("=" * 60)

try:
    from models.sentiment_model import LightweightSentimentAnalyzer
    
    analyzer = LightweightSentimentAnalyzer()
    
    test_texts = {
        'Sehr positiv': "Das ist ein ausgezeichneter Artikel! Super hilfreich und informativ. Großartig!",
        'Positiv': "Guter Artikel, hat mir geholfen.",
        'Neutral': "Das ist ein Artikel.",
        'Negativ': "Leider sehr schlecht erklärt.",
        'Sehr negativ': "Furchtbar! Völlig unverständlich und nutzlos. Schrecklich geschrieben!"
    }
    
    for label, text in test_texts.items():
        result = analyzer.analyze(text)
        print(f"\n{label}:")
        print(f"  Text: {text}")
        print(f"  Score: {result['score']}")
        print(f"  Kategorie: {result['category']}")
        print(f"  Confidence: {result['confidence']}")
    
    print("\n✓ Sentiment Model Test erfolgreich")
    
except Exception as e:
    print(f"\n✗ Sentiment Model Test fehlgeschlagen: {e}")
    sys.exit(1)


# Test 2: Article Categorizer
print("\n" + "=" * 60)
print("TEST 2: Article Categorizer")
print("=" * 60)

try:
    from src.article_categorizer import ArticleCategorizer
    
    categorizer = ArticleCategorizer()
    
    test_article = {
        'title': 'Neue HR Software-Einführung',
        'content': 'Wir führen eine neue Software für das Personal-Management ein. '
                  'Das IT-Team hat die Technologie bereits getestet. '
                  'Alle Mitarbeiter werden geschult.'
    }
    
    categories = categorizer.categorize_by_content(
        test_article['title'],
        test_article['content']
    )
    
    print(f"\nArtikel: {test_article['title']}")
    print(f"Erkannte Kategorien:")
    for cat, score in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {score:.3f}")
    
    keywords = categorizer.extract_keywords(
        test_article['title'] + ' ' + test_article['content']
    )
    print(f"\nExtrahierte Keywords: {keywords[:5]}")
    
    print("\n✓ Article Categorizer Test erfolgreich")
    
except Exception as e:
    print(f"\n✗ Article Categorizer Test fehlgeschlagen: {e}")
    sys.exit(1)


# Test 3: Integration Test
print("\n" + "=" * 60)
print("TEST 3: Integration Test")
print("=" * 60)

try:
    from src.sentiment_analyzer import SentimentAnalyzer
    
    analyzer = SentimentAnalyzer()
    
    test_comments = [
        "Sehr guter Artikel!",
        "Super hilfreich, danke!",
        "Ganz okay.",
        "Leider nicht so gut.",
        "Unverständlich geschrieben."
    ]
    
    result = analyzer.analyze_comments_for_article(test_comments)
    
    print(f"\nAnzahl Kommentare: {result['total_comments']}")
    print(f"Durchschn. Sentiment: {result['avg_score']}")
    print(f"Gesamt-Kategorie: {result['overall_category']}")
    print(f"Sentiment-Verteilung: {result['sentiment_distribution']}")
    print(f"Positive Ratio: {result['positive_ratio']}")
    print(f"Negative Ratio: {result['negative_ratio']}")
    
    print("\n✓ Integration Test erfolgreich")
    
except Exception as e:
    print(f"\n✗ Integration Test fehlgeschlagen: {e}")
    sys.exit(1)


print("\n" + "=" * 60)
print("ALLE TESTS ERFOLGREICH!")
print("=" * 60)
print("\nDas System ist bereit für den Einsatz.")
print("Führe 'python main.py --help' für weitere Informationen aus.")
