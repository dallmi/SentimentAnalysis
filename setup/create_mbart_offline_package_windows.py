"""
Create mBART offline package for Windows Python 3.12

This downloads all dependencies needed for mBART on Windows.

Usage:
    python create_mbart_offline_package_windows.py
"""

import subprocess
import sys
from pathlib import Path


def create_mbart_offline_package():
    """
    Download mBART dependencies for Windows Python 3.12 offline installation.
    """
    print("=" * 70)
    print("CREATING mBART OFFLINE PACKAGE FOR WINDOWS PYTHON 3.12")
    print("=" * 70)

    # Output directory
    base_dir = Path(__file__).parent.parent
    offline_dir = base_dir / "offline_packages" / "mbart_windows_py312"
    offline_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nOutput directory: {offline_dir}")

    # Packages required for mBART
    packages = [
        "transformers",
        "torch",
        "sentencepiece",
        "protobuf",
        "sacremoses",
        "tokenizers"
    ]

    print(f"\nPackages to download: {', '.join(packages)}")
    print("\nDownloading wheels for:")
    print("  Platform: win_amd64")
    print("  Python: 3.12")
    print("\nThis will download ~500-800 MB...")

    try:
        # Download packages for Windows Python 3.12
        cmd = [
            sys.executable, "-m", "pip", "download",
            "--dest", str(offline_dir),
            "--platform", "win_amd64",
            "--python-version", "312",
            "--only-binary", ":all:",
            *packages
        ]

        print(f"\nRunning: {' '.join(cmd)}")
        print("\n" + "=" * 70)

        result = subprocess.run(cmd, check=True, capture_output=False)

        print("\n" + "=" * 70)
        print("SUCCESS! Offline package created")
        print("=" * 70)

        # Count files
        wheel_files = list(offline_dir.glob("*.whl"))
        total_size = sum(f.stat().st_size for f in wheel_files) / (1024 * 1024)

        print(f"\nStatistics:")
        print(f"  Location: {offline_dir}")
        print(f"  Files: {len(wheel_files)} wheel files")
        print(f"  Total size: {total_size:.1f} MB")

        print("\nNext steps:")
        print("  1. This package is ready for offline deployment")
        print("  2. Transfer 'offline_packages/mbart_windows_py312' to Windows machine")
        print("  3. Install with:")
        print(f"     cd {offline_dir.name}")
        print("     pip install --no-index --find-links . transformers sentencepiece")

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading packages: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_mbart_offline_package()
    sys.exit(0 if success else 1)
