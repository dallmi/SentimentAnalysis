"""
Test-Skript für Offline Sentiment Analyzer
Testet ob die lokal gespeicherten Models korrekt funktionieren
"""

import sys
from pathlib import Path

# Füge aktuelles Verzeichnis zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from offline_sentiment_analyzer import OfflineSentimentAnalyzer
import json


def print_section(title: str):
    """Druckt Section-Header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_model_availability():
    """Testet ob Model verfügbar ist"""
    print_section("TEST 1: Model Availability")

    models_dir = Path(__file__).parent / "models"

    if not models_dir.exists():
        print("✗ models/ Ordner nicht gefunden!")
        print(f"  Erwartet in: {models_dir}")
        print("\n  AKTION ERFORDERLICH:")
        print("  1. In privater Umgebung mit Internet:")
        print("     python download_model.py")
        print("  2. Committen und pushen zu Git")
        print("  3. In Corporate-Umgebung: git pull")
        return False

    # Suche nach Model-Dateien
    model_dirs = [
        models_dir / "sentiment-multilingual",  # Trainiertes Sentiment-Model
        models_dir / "distilbert-multilingual",
        models_dir / "distilbert-small"
    ]

    found_models = []
    for model_dir in model_dirs:
        if model_dir.exists() and (model_dir / "config.json").exists():
            found_models.append(model_dir)
            print(f"✓ Model gefunden: {model_dir.name}")

            # Zeige Metadata
            metadata_file = model_dir / "model_info.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    print(f"  - Größe: {metadata.get('size_mb', 0):.1f} MB")
                    print(f"  - Sprachen: {', '.join(metadata.get('languages', [])[:5])}")

            # Zeige Dateien
            config_file = model_dir / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    print(f"  - Model Type: {config.get('model_type', 'unknown')}")
                    print(f"  - Vocab Size: {config.get('vocab_size', 0)}")

    if not found_models:
        print("\n✗ Keine Models gefunden!")
        print("  Bitte führe zuerst download_model.py aus.")
        return False

    print(f"\n✓ {len(found_models)} Model(s) verfügbar")
    return True


def test_offline_mode():
    """Testet ob Analyzer im Offline-Modus läuft"""
    print_section("TEST 2: Offline Mode")

    print("Initialisiere Analyzer im Offline-Modus...")

    try:
        analyzer = OfflineSentimentAnalyzer()
        print(f"✓ Analyzer initialisiert")
        print(f"  Modus: {analyzer.mode}")

        info = analyzer.get_info()
        print(f"\nAnalyzer Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")

        if analyzer.mode == 'distilbert':
            print("\n✓ DistilBERT Model erfolgreich geladen (offline)")
            return True
        elif analyzer.mode == 'bert':
            print("\n✓ BERT Model erfolgreich geladen (offline)")
            return True
        elif analyzer.mode == 'lexicon':
            print("\n⚠ Fallback auf Lexikon-Modus")
            print("  (Transformer-Model nicht verfügbar, aber funktioniert)")
            return True
        else:
            print(f"\n✗ Unbekannter Modus: {analyzer.mode}")
            return False

    except Exception as e:
        print(f"\n✗ Fehler beim Initialisieren: {e}")
        return False


def test_multilingual_analysis():
    """Testet Multi-Language Sentiment-Analyse"""
    print_section("TEST 3: Multilingual Analysis")

    analyzer = OfflineSentimentAnalyzer()

    test_cases = [
        # (Sprache, Text, Erwartetes Sentiment)
        ("English", "This is an excellent article! Very helpful.", "positive"),
        ("English", "This is terrible and useless.", "negative"),
        ("German", "Das ist ein hervorragender Artikel!", "positive"),
        ("German", "Das ist schrecklich und nutzlos.", "negative"),
        ("French", "C'est un excellent article!", "positive"),
        ("French", "C'est terrible et inutile.", "negative"),
        ("Italian", "Questo è un ottimo articolo!", "positive"),
        ("Italian", "Questo è terribile e inutile.", "negative"),
    ]

    correct = 0
    total = len(test_cases)

    print(f"\nAnalysiere {total} Texte in 4 Sprachen...\n")

    for lang, text, expected in test_cases:
        result = analyzer.analyze(text)

        # Prüfe ob Sentiment korrekt erkannt wurde
        is_correct = (
            (expected == "positive" and result['score'] > 0) or
            (expected == "negative" and result['score'] < 0)
        )

        status = "✓" if is_correct else "✗"
        emoji = "😊" if result['score'] > 0 else "😐" if result['score'] == 0 else "😞"

        if is_correct:
            correct += 1

        print(f"{status} {emoji} [{lang:7s}] {text[:50]:50s}")
        print(f"     Score: {result['score']:+.3f}, Expected: {expected:8s}, "
              f"Got: {result['category']:8s}, Confidence: {result['confidence']:.3f}")

    accuracy = correct / total
    print(f"\n{'='*70}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")

    if analyzer.mode in ['distilbert', 'bert']:
        threshold = 0.75  # Transformer-Models sollten >75% haben
    else:
        threshold = 0.70  # Lexikon-Modus etwas niedriger

    if accuracy >= threshold:
        print(f"✓ Test bestanden (Accuracy >= {threshold:.0%})")
        return True
    else:
        print(f"✗ Test fehlgeschlagen (Accuracy < {threshold:.0%})")
        return False


def test_batch_processing():
    """Testet Batch-Verarbeitung"""
    print_section("TEST 4: Batch Processing")

    analyzer = OfflineSentimentAnalyzer()

    comments = [
        "Great article, very helpful!",
        "Excellent explanation, thank you!",
        "Not clear, confusing content.",
        "Perfect overview!",
        "Terrible, waste of time.",
        "Good structure and examples.",
        "Very informative.",
        "Poorly written and unclear.",
    ]

    print(f"Analysiere {len(comments)} Kommentare als Batch...\n")

    try:
        aggregate = analyzer.get_aggregate_sentiment(comments)

        print("Ergebnisse:")
        print(f"  Average Score: {aggregate['avg_score']:+.3f}")
        print(f"  Median Score: {aggregate['median_score']:+.3f}")
        print(f"  Total Texts: {aggregate['total_texts']}")
        print(f"  Positive: {aggregate['positive_ratio']:.1%}")
        print(f"  Negative: {aggregate['negative_ratio']:.1%}")
        print(f"  Neutral: {aggregate['neutral_ratio']:.1%}")
        print(f"  Mode: {aggregate['mode']}")

        print("\n✓ Batch-Verarbeitung erfolgreich")
        return True

    except Exception as e:
        print(f"\n✗ Fehler bei Batch-Verarbeitung: {e}")
        return False


def test_performance():
    """Testet Performance"""
    print_section("TEST 5: Performance")

    import time

    analyzer = OfflineSentimentAnalyzer()

    test_text = "This is a great article with excellent content and very helpful information."

    # Warmup
    analyzer.analyze(test_text)

    # Measure single text
    start = time.time()
    for _ in range(10):
        analyzer.analyze(test_text)
    duration = time.time() - start
    avg_time = duration / 10

    print(f"Einzeltext-Verarbeitung:")
    print(f"  Durchschnitt: {avg_time*1000:.2f} ms pro Text")
    print(f"  Durchsatz: {1/avg_time:.1f} Texte/Sekunde")

    # Measure batch
    batch_texts = [test_text] * 50

    start = time.time()
    analyzer.analyze_batch(batch_texts)
    duration = time.time() - start
    avg_batch_time = duration / 50

    print(f"\nBatch-Verarbeitung (50 Texte):")
    print(f"  Gesamt: {duration:.2f} Sekunden")
    print(f"  Durchschnitt: {avg_batch_time*1000:.2f} ms pro Text")
    print(f"  Durchsatz: {1/avg_batch_time:.1f} Texte/Sekunde")

    if analyzer.mode in ['distilbert', 'bert']:
        print(f"\nModus: {analyzer.mode.upper()} (erwartbar: 10-100 ms/Text)")
    else:
        print(f"\nModus: Lexikon (erwartbar: <1 ms/Text)")

    print("\n✓ Performance-Test abgeschlossen")
    return True


def run_all_tests():
    """Führt alle Tests aus"""
    print("\n" + "="*70)
    print("  OFFLINE SENTIMENT ANALYZER - TEST SUITE")
    print("="*70)

    tests = [
        ("Model Availability", test_model_availability),
        ("Offline Mode", test_offline_mode),
        ("Multilingual Analysis", test_multilingual_analysis),
        ("Batch Processing", test_batch_processing),
        ("Performance", test_performance),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))

            # Wenn kritischer Test fehlschlägt, abbrechen
            if not success and test_name in ["Model Availability", "Offline Mode"]:
                print(f"\n⚠ Kritischer Test fehlgeschlagen. Weitere Tests übersprungen.")
                break

        except Exception as e:
            print(f"\n✗ Test '{test_name}' fehlgeschlagen mit Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status:10s} {test_name}")

    print(f"\n  Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n  🎉 Alle Tests erfolgreich!")
        print("\n  Der Offline Sentiment Analyzer ist bereit für Corporate-Einsatz!")
        return True
    else:
        print(f"\n  ⚠️  {total - passed} Test(s) fehlgeschlagen")
        print("\n  NÄCHSTE SCHRITTE:")

        if not any(name == "Model Availability" and success for name, success in results):
            print("  1. Führe download_model.py in privater Umgebung aus")
            print("  2. Committe models/ Ordner zu Git")
            print("  3. In Corporate-Umgebung: git pull")

        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
