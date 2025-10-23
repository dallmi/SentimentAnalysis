#!/usr/bin/env python3
"""
Download BERTopic and all dependencies for WINDOWS offline installation
This script downloads wheel files compatible with Windows (win_amd64)
"""

import subprocess
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

def create_offline_package():
    """Download all required packages for Windows offline installation."""

    print("=" * 70)
    print("BERTopic Offline Package Creator - WINDOWS VERSION")
    print("=" * 70)
    print("\nThis script will download:")
    print("  - bertopic")
    print("  - sentence-transformers")
    print("  - umap-learn")
    print("  - hdbscan")
    print("  - All dependencies")
    print("\nPlatform: Windows (win_amd64)")
    print("Python: 3.9, 3.10, 3.11, 3.12 compatible")
    print("Estimated download size: ~500MB")
    print("\nStarting download...")

    # Create offline packages directory for Windows
    offline_dir = Path(__file__).parent / "offline_packages" / "bertopic_windows"
    offline_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[1/3] Downloading packages to {offline_dir}...")

    # List of packages to download
    packages = [
        "bertopic",
        "sentence-transformers",
        "umap-learn",
        "hdbscan",
        "plotly",
        "kaleido",
        "pandas",
        "numpy",
        "scikit-learn",
        "scipy",
        "torch",
        "transformers"
    ]

    try:
        # Download packages with pip download
        # --platform win_amd64 ensures Windows compatibility
        # --python-version 39 targets Python 3.9+ (works for 3.9-3.12)
        subprocess.run([
            sys.executable, "-m", "pip", "download",
            "--dest", str(offline_dir),
            "--platform", "win_amd64",
            "--python-version", "39",
            "--only-binary", ":all:",
            *packages
        ], check=True)

        print("\n✓ All packages downloaded successfully!")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading packages: {e}")
        print("\nNote: Some packages might not be available for the specified platform.")
        print("Try running this script on a Windows machine instead.")
        return

    # Download pre-trained models
    print("\n[2/3] Downloading pre-trained models...")
    models_dir = Path(__file__).parent / "offline_packages" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    model_names = [
        "all-MiniLM-L6-v2",                               # Fast English model
        "paraphrase-multilingual-MiniLM-L12-v2"          # Multilingual (50+ languages)
    ]

    for model_name in model_names:
        print(f"  Downloading {model_name}...")
        try:
            model = SentenceTransformer(model_name)
            model_path = models_dir / model_name
            model.save(str(model_path))
            print(f"  ✓ Saved to {model_path}")
        except Exception as e:
            print(f"  ❌ Error downloading {model_name}: {e}")

    # Create installation script for Windows
    print("\n[3/3] Creating installation script...")

    install_script_bat = offline_dir.parent / "install_bertopic_offline_windows.bat"
    with open(install_script_bat, 'w') as f:
        f.write("""@echo off
REM BERTopic Offline Installation Script for Windows
REM This script installs BERTopic and all dependencies from local wheel files

echo ============================================
echo BERTopic Offline Installation (Windows)
echo ============================================
echo.

cd /d "%~dp0bertopic_windows"

echo Installing BERTopic and dependencies...
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo Installation successful!
    echo ============================================
    echo.
    echo You can now use BERTopic offline.
    echo Models are in: offline_packages/models/
    echo.
) else (
    echo.
    echo ============================================
    echo Installation failed!
    echo ============================================
    echo.
    echo Check the error messages above.
    echo.
)

pause
""")

    print(f"✓ Created {install_script_bat}")

    # Create README
    readme_path = offline_dir / "README_WINDOWS.txt"
    with open(readme_path, 'w') as f:
        f.write("""BERTopic Offline Installation Package for Windows
==================================================

This package contains all files needed to install BERTopic offline on Windows.

INSTALLATION:
-------------
1. Copy this entire folder to your Windows PC
2. Open Command Prompt (cmd.exe)
3. Navigate to the offline_packages folder
4. Run: install_bertopic_offline_windows.bat

OR manually:
   cd offline_packages\\bertopic_windows
   pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan

MODELS:
-------
Pre-trained models are in: offline_packages/models/
- all-MiniLM-L6-v2 (English, fast)
- paraphrase-multilingual-MiniLM-L12-v2 (50+ languages incl. German)

USAGE:
------
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Load multilingual model
model = SentenceTransformer('offline_packages/models/paraphrase-multilingual-MiniLM-L12-v2')
topic_model = BERTopic(embedding_model=model)

# Analyze documents
docs = ["Your text here", "Another document"]
topics, probs = topic_model.fit_transform(docs)

REQUIREMENTS:
-------------
- Windows 7/10/11 (64-bit)
- Python 3.9 or newer
- pip installed

For more information, see BERTOPIC_OFFLINE_INSTALL.md
""")

    print(f"✓ Created {readme_path}")

    # Print summary
    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETE!")
    print("=" * 70)

    # Count files
    wheel_files = list(offline_dir.glob("*.whl"))
    total_size = sum(f.stat().st_size for f in wheel_files) / (1024 * 1024)

    print(f"\nTotal files downloaded: {len(wheel_files)}")
    print(f"Total size: {total_size:.1f} MB")
    print(f"\nFiles saved to: {offline_dir}")

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("\n1. Transfer to Windows Corporate PC:")
    print("   - Copy the entire 'offline_packages' folder")
    print("   - Use USB drive, file share, or approved transfer method")

    print("\n2. Install on Windows:")
    print("   - Run: install_bertopic_offline_windows.bat")
    print("   - Or manually:")
    print(f"     cd {offline_dir}")
    print("     pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan")

    print("\n3. Models are ready in:")
    print(f"   {models_dir}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    create_offline_package()
