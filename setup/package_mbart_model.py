"""
Package mBART-large-50 model for offline distribution

This script creates a ZIP file containing the mBART model for
distribution via GitHub Releases.

Usage:
    1. First download the model: python download_mbart_model.py
    2. Then package it: python package_mbart_model.py
"""

import os
import shutil
from pathlib import Path
import zipfile


def package_mbart_model():
    """
    Package the mBART model into a ZIP file for GitHub Release.
    """
    print("=" * 70)
    print("PACKAGING mBART-LARGE-50 MODEL FOR OFFLINE DISTRIBUTION")
    print("=" * 70)

    # Paths
    base_dir = Path(__file__).parent.parent
    model_dir = base_dir / "LLM Solution" / "models" / "mbart-large-50"
    output_dir = base_dir / "offline_packages"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "mbart-large-50-model.zip"

    # Check if model exists
    if not model_dir.exists():
        print(f"\n❌ Error: Model not found at {model_dir}")
        print("\nPlease download the model first:")
        print("  python setup/download_mbart_model.py")
        return False

    print(f"\nModel location: {model_dir}")
    print(f"Output file: {output_file}")

    # Get model files
    model_files = list(model_dir.glob("*"))
    if not model_files:
        print(f"\n❌ Error: No files found in {model_dir}")
        return False

    print(f"\nFound {len(model_files)} model files")
    print("\nPackaging files:")
    for f in model_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  - {f.name} ({size_mb:.1f} MB)")

    # Create ZIP file
    print(f"\nCreating ZIP file...")
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for file_path in model_files:
                if file_path.is_file():
                    arcname = f"mbart-large-50/{file_path.name}"
                    zipf.write(file_path, arcname=arcname)
                    print(f"  ✓ Added: {file_path.name}")

        # Get final size
        final_size_mb = output_file.stat().st_size / (1024 * 1024)

        print("\n" + "=" * 70)
        print("SUCCESS! Model packaged")
        print("=" * 70)
        print(f"\nOutput file: {output_file}")
        print(f"File size: {final_size_mb:.1f} MB")
        print("\nNext steps:")
        print("  1. Upload to GitHub Release:")
        print(f"     gh release upload v1.0-abstractive {output_file}")
        print("  2. Users can download and extract:")
        print("     unzip mbart-large-50-model.zip")
        print('     mv mbart-large-50 "LLM Solution/models/"')

        return True

    except Exception as e:
        print(f"\n❌ Error during packaging: {e}")
        return False


if __name__ == "__main__":
    package_mbart_model()
