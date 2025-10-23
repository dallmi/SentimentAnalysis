"""
Download mBART-large-50 for abstractive summarization
Supports 50 languages including German

Usage:
    python download_mbart_model.py
"""

import os
from pathlib import Path
from transformers import MBartForConditionalGeneration, MBart50Tokenizer

def download_mbart_model():
    """
    Download mBART-large-50 model for abstractive summarization.

    Model: facebook/mbart-large-50-many-to-many-mmt
    Size: ~2.4 GB
    Languages: 50+ including German, English, French, Italian, Spanish
    """

    # Model path
    model_name = "facebook/mbart-large-50-many-to-many-mmt"

    # Save location
    base_dir = Path(__file__).parent.parent
    save_dir = base_dir / "LLM Solution" / "models" / "mbart-large-50"
    save_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("DOWNLOADING mBART-large-50 MODEL FOR ABSTRACTIVE SUMMARIZATION")
    print("=" * 70)
    print(f"\nModel: {model_name}")
    print(f"Size: ~2.4 GB")
    print(f"Languages: 50+ (including German 🇩🇪)")
    print(f"Save location: {save_dir}")
    print("\n" + "=" * 70)

    try:
        print("\n[1/2] Downloading tokenizer...")
        tokenizer = MBart50Tokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(save_dir)
        print("   ✓ Tokenizer downloaded")

        print("\n[2/2] Downloading model (this will take several minutes)...")
        model = MBartForConditionalGeneration.from_pretrained(model_name)
        model.save_pretrained(save_dir)
        print("   ✓ Model downloaded")

        print("\n" + "=" * 70)
        print("SUCCESS! Model ready for offline use")
        print("=" * 70)
        print(f"\nModel location: {save_dir}")
        print("\nYou can now use abstractive summarization in main_bertopic.py:")
        print("  python main_bertopic.py --input data.json --abstractive")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("  - Check internet connection")
        print("  - Install transformers: pip install transformers")
        print("  - Check disk space (need ~3 GB free)")
        return False

    return True


if __name__ == "__main__":
    download_mbart_model()
