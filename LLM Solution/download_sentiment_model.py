"""
Download eines bereits für Sentiment-Analyse trainierten Models
"""

import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import json

def download_sentiment_model():
    """Lädt ein für Sentiment bereits trainiertes Model"""
    print("="*70)
    print("  LADE SENTIMENT-ANALYSIS MODEL")
    print("="*70)

    # Verwende ein bereits für Sentiment trainiertes Model
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    save_dir = Path(__file__).parent / "models" / "sentiment-multilingual"

    print(f"\nModel: {model_name}")
    print(f"Beschreibung: Multilingual Sentiment (5-Star Rating)")
    print(f"Sprachen: EN, DE, FR, IT, ES, NL")
    print(f"Ziel: {save_dir}")

    save_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1/3] Lade Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(save_dir)
    print("     ✓ Tokenizer gespeichert")

    print("\n[2/3] Lade Model (~650 MB Download)...")
    print("     Dies kann einige Minuten dauern...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.save_pretrained(save_dir)
    print("     ✓ Model gespeichert")

    print("\n[3/3] Teste Model...")
    # Quick test
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer
    )

    test_texts = [
        "This is excellent!",
        "This is terrible.",
        "Das ist großartig!",
        "Das ist schrecklich."
    ]

    print("\n     Quick Test:")
    for text in test_texts:
        result = sentiment_pipeline(text)[0]
        print(f"       '{text}' -> {result['label']} ({result['score']:.3f})")

    print("\n[4/4] Erstelle Metadata...")
    metadata = {
        "model_name": model_name,
        "model_type": "bert",
        "task": "sentiment-analysis",
        "languages": ["en", "de", "fr", "it", "es", "nl"],
        "num_labels": 5,
        "labels": ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"],
        "description": "Fine-tuned on multilingual product reviews (5-star rating)",
        "size_mb": sum(f.stat().st_size for f in save_dir.rglob('*') if f.is_file()) / (1024*1024)
    }

    with open(save_dir / "model_info.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    print("     ✓ Metadata gespeichert")

    total_size = sum(f.stat().st_size for f in save_dir.rglob('*') if f.is_file()) / (1024*1024)

    print("\n" + "="*70)
    print("  ✓ DOWNLOAD ERFOLGREICH!")
    print("="*70)
    print(f"\nGesamt-Größe: {total_size:.1f} MB")
    print(f"Speicherort: {save_dir}")

    print("\nHeruntergeladene Dateien:")
    for file in sorted(save_dir.rglob('*')):
        if file.is_file():
            size = file.stat().st_size / (1024*1024)
            print(f"  {file.name:40s} {size:8.2f} MB")

    return True

if __name__ == "__main__":
    try:
        success = download_sentiment_model()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
