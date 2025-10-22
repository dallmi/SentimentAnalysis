"""
Automatischer Model Download (non-interactive)
"""

import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

def download_distilbert_multilingual():
    """Lädt DistilBERT Multilingual"""
    print("="*70)
    print("  LADE DISTILBERT MULTILINGUAL MODEL")
    print("="*70)

    model_name = "distilbert-base-multilingual-cased"
    save_dir = Path(__file__).parent / "models" / "distilbert-multilingual"

    print(f"\nModel: {model_name}")
    print(f"Ziel: {save_dir}")

    save_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1/3] Lade Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(save_dir)
    print("     ✓ Tokenizer gespeichert")

    print("\n[2/3] Lade Model (~270 MB Download)...")
    print("     Dies kann einige Minuten dauern...")
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=3
    )
    model.save_pretrained(save_dir)
    print("     ✓ Model gespeichert")

    print("\n[3/3] Erstelle Metadata...")
    metadata = {
        "model_name": model_name,
        "model_type": "distilbert",
        "task": "sentiment-analysis",
        "languages": ["en", "de", "fr", "it", "es", "nl", "pl", "pt", "ru", "zh"],
        "num_labels": 3,
        "labels": ["negative", "neutral", "positive"],
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

    # Liste Dateien
    print("\nHeruntergeladene Dateien:")
    for file in sorted(save_dir.rglob('*')):
        if file.is_file():
            size = file.stat().st_size / (1024*1024)
            print(f"  {file.name:40s} {size:8.2f} MB")

    return True

if __name__ == "__main__":
    try:
        success = download_distilbert_multilingual()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
