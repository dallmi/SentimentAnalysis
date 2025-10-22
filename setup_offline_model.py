"""
Setup script to download BERT model for offline use in corporate environments.
Downloads the multilingual sentiment analysis model and saves it locally.

Usage:
    python setup_offline_model.py

For corporate proxy:
    Edit this file and set proxy environment variables before running.
"""

import os
import sys
from pathlib import Path


def setup_proxy_if_needed():
    """
    Configure proxy if needed for corporate environments.
    Edit these values according to your corporate proxy settings.
    """
    # Uncomment and edit if you need proxy:
    # os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
    # os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'
    pass


def check_internet_connection():
    """Check if internet connection is available."""
    import urllib.request

    try:
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False


def download_model():
    """Download the BERT model from HuggingFace."""

    print("="*70)
    print("  BERT MODEL SETUP FOR OFFLINE USE")
    print("="*70)

    # Check internet
    print("\n[1/4] Checking internet connection...")
    if not check_internet_connection():
        print("✗ No internet connection detected!")
        print("\n  If you're behind a corporate proxy:")
        print("  1. Edit this file (setup_offline_model.py)")
        print("  2. Uncomment and set HTTP_PROXY/HTTPS_PROXY in setup_proxy_if_needed()")
        print("  3. Run again")
        print("\n  Or use Option C from README: Manual download")
        return False
    print("✓ Internet connection available")

    # Import transformers
    print("\n[2/4] Checking dependencies...")
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        print("✓ transformers library available")
    except ImportError:
        print("✗ transformers library not found!")
        print("\n  Install with: pip install transformers torch")
        return False

    # Create models directory
    print("\n[3/4] Creating models directory...")
    models_dir = Path(__file__).parent / "models"
    model_path = models_dir / "bert-base-multilingual-uncased-sentiment"

    models_dir.mkdir(exist_ok=True)
    print(f"✓ Models directory: {models_dir}")

    # Download model
    print("\n[4/4] Downloading BERT model (~600MB)...")
    print("     This may take 5-10 minutes depending on your connection...")

    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"

    try:
        print(f"\n  Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(model_path)
        print(f"  ✓ Tokenizer saved")

        print(f"\n  Downloading model (this is the large file ~600MB)...")
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.save_pretrained(model_path)
        print(f"  ✓ Model saved")

        print(f"\n{'='*70}")
        print(f"  SUCCESS!")
        print(f"{'='*70}")
        print(f"\nModel saved to: {model_path}")
        print(f"\nVerify installation:")
        print(f"  - Check folder: ls {model_path}")
        print(f"  - Should contain: config.json, pytorch_model.bin, vocab.txt, etc.")

        # Show file sizes
        if model_path.exists():
            total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
            print(f"  - Total size: {total_size / (1024*1024):.1f} MB")

        print(f"\nNext steps:")
        print(f"  1. Run test: python LLM\\ Solution/test_offline_model.py")
        print(f"  2. Analyze articles: python main.py --input data/input/your_file.xlsx")

        print(f"\nFor corporate deployment:")
        print(f"  - The models/ folder is now ready for offline use")
        print(f"  - You can commit this to git (if git-lfs is configured)")
        print(f"  - Or transfer the models/ folder manually to corporate environment")

        return True

    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        print(f"\nTroubleshooting:")
        print(f"  - Check internet connection")
        print(f"  - If behind proxy, configure proxy settings in this file")
        print(f"  - Try manual download (see README - Option C)")
        return False


def main():
    """Main setup function."""

    # Setup proxy if needed
    setup_proxy_if_needed()

    # Download model
    success = download_model()

    if success:
        print("\n✅ Setup complete! Model is ready for offline use.")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. See error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
