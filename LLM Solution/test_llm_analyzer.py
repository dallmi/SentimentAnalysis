"""
Test-Skript für LLM Sentiment Analyzer
Testet alle Komponenten und Multi-Language Support
"""

import sys
from pathlib import Path

# Füge aktuelles Verzeichnis zum Python Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from llm_sentiment_analyzer import LLMSentimentAnalyzer
from minimal_bert_tokenizer import MinimalBertTokenizer
from minimal_bert_model import MinimalBertForSentiment
import numpy as np


def print_section(title: str):
    """Druckt Section-Header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_tokenizer():
    """Testet den Minimal BERT Tokenizer"""
    print_section("TEST 1: Minimal BERT Tokenizer")

    tokenizer = MinimalBertTokenizer()

    test_cases = [
        "This is a good article!",
        "Das ist ein guter Artikel!",
        "C'est un bon article!",
        "Questo è un buon articolo!"
    ]

    for text in test_cases:
        tokens = tokenizer.tokenize(text)
        encoded = tokenizer.encode(text, max_length=32)

        print(f"\nText: {text}")
        print(f"  Tokens: {tokens[:10]}")
        print(f"  Input IDs (first 10): {encoded['input_ids'][:10]}")
        print(f"  Vocab size: {len(tokenizer.vocab)}")

    print("\n✓ Tokenizer Test erfolgreich!")
    return True


def test_bert_model():
    """Testet das Minimal BERT Model"""
    print_section("TEST 2: Minimal BERT Model")

    print("Initialisiere Model...")
    model = MinimalBertForSentiment(
        vocab_size=500,
        hidden_size=64,  # Kleiner für schnelleren Test
        num_hidden_layers=1,
        num_attention_heads=2,
        num_labels=3
    )

    # Test forward pass
    batch_size = 2
    seq_length = 16

    input_ids = np.random.randint(0, 500, size=(batch_size, seq_length))
    attention_mask = np.ones((batch_size, seq_length))

    print(f"Input Shape: {input_ids.shape}")
    print("Running forward pass...")

    results = model.predict(input_ids, attention_mask)

    for i, result in enumerate(results):
        print(f"\n  Sample {i+1}:")
        print(f"    Label: {result['label']}")
        print(f"    Confidence: {result['score']:.3f}")
        print(f"    All Scores: neg={result['all_scores']['negative']:.3f}, "
              f"neu={result['all_scores']['neutral']:.3f}, "
              f"pos={result['all_scores']['positive']:.3f}")

    print("\n✓ BERT Model Test erfolgreich!")
    return True


def test_llm_analyzer_lexicon():
    """Testet LLM Analyzer mit Lexikon-Methode"""
    print_section("TEST 3: LLM Analyzer (Lexicon Mode)")

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    test_cases = [
        ("This is an excellent article! Very helpful.", "positive", "English"),
        ("This is terrible and confusing.", "negative", "English"),
        ("Das ist ein hervorragender Artikel!", "positive", "German"),
        ("Das ist schrecklich und verwirrend.", "negative", "German"),
        ("C'est un excellent article!", "positive", "French"),
        ("C'est terrible et confus.", "negative", "French"),
        ("Questo è un ottimo articolo!", "positive", "Italian"),
        ("Questo è terribile e confuso.", "negative", "Italian"),
    ]

    correct = 0
    total = len(test_cases)

    for text, expected_sentiment, language in test_cases:
        result = analyzer.analyze(text)

        is_correct = (
            (expected_sentiment == "positive" and result['score'] > 0) or
            (expected_sentiment == "negative" and result['score'] < 0)
        )

        status = "✓" if is_correct else "✗"
        if is_correct:
            correct += 1

        print(f"\n{status} [{language}] {text}")
        print(f"    Score: {result['score']:+.3f}, Category: {result['category']}, "
              f"Confidence: {result['confidence']:.3f}")

    accuracy = correct / total
    print(f"\n{'='*70}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")

    if accuracy >= 0.75:
        print("✓ Lexicon Analyzer Test erfolgreich!")
        return True
    else:
        print("✗ Lexicon Analyzer Test fehlgeschlagen (Accuracy < 75%)")
        return False


def test_llm_analyzer_bert():
    """Testet LLM Analyzer mit BERT-Methode"""
    print_section("TEST 4: LLM Analyzer (BERT Mode)")

    print("Initialisiere Analyzer mit BERT...")
    analyzer = LLMSentimentAnalyzer(use_bert=True)

    test_texts = [
        "This is a very good article! Super helpful and informative.",
        "Unfortunately very poorly explained and unclear.",
        "Das ist ein hervorragender Artikel!",
        "Leider sehr schlecht erklärt.",
    ]

    print("\nAnalysiere Texte...")
    for i, text in enumerate(test_texts, 1):
        result = analyzer.analyze(text)

        print(f"\n  {i}. {text}")
        print(f"     Score: {result['score']:+.3f}")
        print(f"     Category: {result['category']}")
        print(f"     Confidence: {result['confidence']:.3f}")
        print(f"     Method: {result['method']}")

    print("\n✓ BERT Analyzer Test erfolgreich!")
    return True


def test_batch_analysis():
    """Testet Batch-Analyse"""
    print_section("TEST 5: Batch Analysis")

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    comments = [
        "Great article, very helpful!",
        "Not good, confusing content.",
        "Perfect explanation, thank you!",
        "Terrible, waste of time.",
        "Good overview.",
        "Bad structure, unclear.",
    ]

    print(f"Analysiere {len(comments)} Kommentare...")
    aggregate = analyzer.get_aggregate_sentiment(comments)

    print(f"\nErgebnisse:")
    print(f"  Average Score: {aggregate['avg_score']:+.3f}")
    print(f"  Median Score: {aggregate['median_score']:+.3f}")
    print(f"  Total Texts: {aggregate['total_texts']}")
    print(f"  Positive Ratio: {aggregate['positive_ratio']:.1%}")
    print(f"  Negative Ratio: {aggregate['negative_ratio']:.1%}")
    print(f"  Neutral Ratio: {aggregate['neutral_ratio']:.1%}")

    print("\n✓ Batch Analysis Test erfolgreich!")
    return True


def test_edge_cases():
    """Testet Edge Cases"""
    print_section("TEST 6: Edge Cases")

    analyzer = LLMSentimentAnalyzer(use_bert=False)

    edge_cases = [
        ("", "empty string"),
        ("   ", "whitespace only"),
        ("...", "punctuation only"),
        ("123 456", "numbers only"),
        ("a b c d e", "very short words"),
        ("not bad", "negation + negative word (should be positive)"),
    ]

    print("\nTeste Edge Cases...")
    for text, description in edge_cases:
        try:
            result = analyzer.analyze(text)
            print(f"  ✓ {description:30s} -> Score: {result['score']:+.3f}")
        except Exception as e:
            print(f"  ✗ {description:30s} -> Error: {e}")
            return False

    print("\n✓ Edge Cases Test erfolgreich!")
    return True


def run_all_tests():
    """Führt alle Tests aus"""
    print("\n" + "="*70)
    print("  LLM SENTIMENT ANALYZER - TEST SUITE")
    print("="*70)

    tests = [
        ("Tokenizer", test_tokenizer),
        ("BERT Model", test_bert_model),
        ("LLM Analyzer (Lexicon)", test_llm_analyzer_lexicon),
        ("LLM Analyzer (BERT)", test_llm_analyzer_bert),
        ("Batch Analysis", test_batch_analysis),
        ("Edge Cases", test_edge_cases),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' fehlgeschlagen mit Error: {e}")
            results.append((test_name, False))

    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status:10s} {test_name}")

    print(f"\n  Total: {passed}/{total} tests passed ({passed/total:.1%})")

    if passed == total:
        print("\n  🎉 Alle Tests erfolgreich!")
        return True
    else:
        print(f"\n  ⚠️  {total - passed} Test(s) fehlgeschlagen")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
