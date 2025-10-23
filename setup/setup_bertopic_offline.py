#!/usr/bin/env python3
"""
Setup BERTopic and dependencies for offline use in corporate environment.

This script downloads all necessary packages and models for BERTopic
so they can be transferred to a corporate network without internet access.

Usage:
    # On your personal computer with internet:
    python setup_bertopic_offline.py

    # Then transfer the entire folder to corporate environment
"""

import os
import sys
import subprocess
from pathlib import Path

def create_offline_package():
    """
    Downloads BERTopic and all dependencies for offline installation.
    """
    print("="*70)
    print("BERTopic Offline Setup")
    print("="*70)
    print("\nThis will download:")
    print("  - bertopic[visualization]")
    print("  - sentence-transformers")
    print("  - umap-learn")
    print("  - hdbscan")
    print("  - All dependencies")
    print("\nEstimated download size: ~500MB")
    print("\nStarting download...")

    # Create offline packages directory
    offline_dir = Path(__file__).parent / "offline_packages" / "bertopic"
    offline_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📦 Downloading packages to: {offline_dir}")

    # List of packages to download
    packages = [
        "bertopic",
        "sentence-transformers",
        "umap-learn",
        "hdbscan",
        "plotly",  # For visualization
        "kaleido",  # For saving plots
        "pandas",
        "numpy",
        "scikit-learn",
        "scipy",
        "torch",  # PyTorch
        "transformers"
    ]

    print(f"\n[1/3] Downloading {len(packages)} packages and dependencies...")

    try:
        # Download packages
        subprocess.run([
            sys.executable, "-m", "pip", "download",
            "--dest", str(offline_dir),
            *packages
        ], check=True)

        print(f"✓ Downloaded packages to {offline_dir}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading packages: {e}")
        return

    # Download pre-trained models
    print("\n[2/3] Downloading pre-trained sentence transformer models...")

    try:
        from sentence_transformers import SentenceTransformer

        models_dir = Path(__file__).parent / "offline_packages" / "models"
        models_dir.mkdir(parents=True, exist_ok=True)

        # Download common models for BERTopic
        model_names = [
            "all-MiniLM-L6-v2",  # Fast, good quality (80MB)
            "paraphrase-multilingual-MiniLM-L12-v2"  # Multilingual (420MB)
        ]

        for model_name in model_names:
            print(f"  Downloading {model_name}...")
            model_path = models_dir / model_name

            # Download model
            model = SentenceTransformer(model_name)
            model.save(str(model_path))

            print(f"  ✓ Saved to {model_path}")

    except Exception as e:
        print(f"⚠️  Could not download models: {e}")
        print("   You can download them later in corporate environment")

    # Create installation instructions
    print("\n[3/3] Creating installation instructions...")

    instructions = f"""# BERTopic Offline Installation Guide

## Files in this package:

1. **offline_packages/bertopic/** - All Python packages (.whl files)
2. **offline_packages/models/** - Pre-trained sentence transformer models
3. **setup_bertopic_offline.py** - This setup script
4. **install_bertopic_offline.sh** - Installation script for corporate environment

## Installation Steps (Corporate Environment):

### Step 1: Transfer Files

Transfer this entire folder to your corporate environment:
- Via USB stick
- Via corporate file share
- Via approved file transfer method

### Step 2: Install Packages

On your corporate machine (Windows):
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

On your corporate machine (Mac/Linux):
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

Or use the installation script:
```bash
bash install_bertopic_offline.sh
```

### Step 3: Verify Installation

```python
# Test if packages are installed
python -c "import bertopic; import sentence_transformers; import umap; import hdbscan; print('✓ All packages installed!')"
```

### Step 4: Use Pre-trained Models

The models are already downloaded in `offline_packages/models/`.

To use them:
```python
from sentence_transformers import SentenceTransformer

# Load offline model
model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')
```

## Troubleshooting

### Missing Dependencies

If you get errors about missing dependencies, install them:
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . *
```

### SSL Certificate Errors

If you get SSL errors when loading models, set:
```python
import os
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
```

### Model Loading Errors

If models don't load, you can download them manually in corporate environment:
```python
from sentence_transformers import SentenceTransformer

# This will download from HuggingFace (if allowed)
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('./offline_packages/models/all-MiniLM-L6-v2')
```

## Package Sizes

- bertopic: ~10MB
- sentence-transformers: ~100MB
- umap-learn: ~50MB
- hdbscan: ~30MB
- Pre-trained models: ~500MB
- Dependencies: ~200MB

**Total: ~900MB**

## Next Steps

After installation, you can use BERTopic in your sentiment analysis:

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Load offline model
sentence_model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')

# Create BERTopic model
topic_model = BERTopic(embedding_model=sentence_model)

# Analyze your articles
topics, probs = topic_model.fit_transform(article_texts)

# Get topic info
topic_model.get_topic_info()
```

## Need Help?

Check the documentation:
- BERTopic: https://maartengr.github.io/BERTopic/
- Sentence Transformers: https://www.sbert.net/

"""

    instructions_file = Path(__file__).parent / "BERTOPIC_OFFLINE_INSTALL.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)

    print(f"✓ Created {instructions_file}")

    # Create installation script
    install_script = """#!/bin/bash
# BERTopic Offline Installation Script

echo "Installing BERTopic and dependencies..."

cd "$(dirname "$0")/offline_packages/bertopic"

pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan plotly kaleido

if [ $? -eq 0 ]; then
    echo "✓ Installation successful!"
    echo ""
    echo "Testing installation..."
    python -c "import bertopic; import sentence_transformers; import umap; import hdbscan; print('✓ All packages work!')"
else
    echo "❌ Installation failed. Try installing dependencies manually:"
    echo "   pip install --no-index --find-links . *"
fi
"""

    install_script_file = Path(__file__).parent / "install_bertopic_offline.sh"
    with open(install_script_file, 'w', encoding='utf-8') as f:
        f.write(install_script)

    # Make executable
    os.chmod(install_script_file, 0o755)

    print(f"✓ Created {install_script_file}")

    # Summary
    print("\n" + "="*70)
    print("SETUP COMPLETE!")
    print("="*70)
    print(f"\nOffline package created in: {offline_dir}")
    print(f"Total files downloaded: {len(list(offline_dir.glob('*')))}")

    total_size = sum(f.stat().st_size for f in offline_dir.glob('*')) / (1024**2)
    print(f"Total size: {total_size:.1f} MB")

    print("\n📋 Next Steps:")
    print("1. Transfer the entire SentimentAnalysis folder to corporate environment")
    print("2. Read BERTOPIC_OFFLINE_INSTALL.md for installation instructions")
    print("3. Run install_bertopic_offline.sh (Mac/Linux) or use pip install (Windows)")

    print("\n💡 Installation command for corporate environment:")
    print("   cd offline_packages/bertopic")
    print("   pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan")

if __name__ == "__main__":
    create_offline_package()
