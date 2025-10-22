"""
Model Download Script für Corporate-Umgebungen
Lädt alle benötigten Model-Dateien lokal herunter
EINMALIG in privater Umgebung mit Internet ausführen!
"""

import os
import sys
from pathlib import Path
import json
import shutil

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
except ImportError:
    print("ERROR: transformers library nicht gefunden!")
    print("Bitte installieren: pip install transformers torch")
    sys.exit(1)


def download_distilbert_multilingual():
    """
    Lädt DistilBERT Multilingual Model und speichert alle Dateien lokal
    """
    print("="*70)
    print("  MODEL DOWNLOAD für Corporate-Umgebungen")
    print("="*70)

    model_name = "distilbert-base-multilingual-cased"
    save_dir = Path(__file__).parent / "models" / "distilbert-multilingual"

    print(f"\nModel: {model_name}")
    print(f"Ziel-Verzeichnis: {save_dir}")

    # Erstelle Verzeichnis
    save_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1/3] Lade Tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(save_dir)
        print("     ✓ Tokenizer gespeichert")
    except Exception as e:
        print(f"     ✗ Fehler beim Tokenizer-Download: {e}")
        return False

    print("\n[2/3] Lade Model...")
    print("     (Dies kann einige Minuten dauern, ~270 MB Download)")
    try:
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=3  # negative, neutral, positive
        )
        model.save_pretrained(save_dir)
        print("     ✓ Model gespeichert")
    except Exception as e:
        print(f"     ✗ Fehler beim Model-Download: {e}")
        return False

    print("\n[3/3] Erstelle Metadata...")
    metadata = {
        "model_name": model_name,
        "model_type": "distilbert",
        "task": "sentiment-analysis",
        "languages": ["en", "de", "fr", "it", "es", "nl", "pl", "pt", "ru", "zh"],
        "num_labels": 3,
        "labels": ["negative", "neutral", "positive"],
        "download_date": str(Path(__file__).stat().st_mtime),
        "size_mb": sum(f.stat().st_size for f in save_dir.rglob('*') if f.is_file()) / (1024*1024)
    }

    metadata_file = save_dir / "model_info.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("     ✓ Metadata gespeichert")

    # Zeige Dateigrößen
    print("\n" + "="*70)
    print("  DOWNLOAD ABGESCHLOSSEN")
    print("="*70)

    total_size = 0
    print("\nHeruntergeladene Dateien:")
    for file in sorted(save_dir.rglob('*')):
        if file.is_file():
            size = file.stat().st_size / (1024*1024)
            total_size += size
            print(f"  {file.name:40s} {size:8.2f} MB")

    print(f"\n  Gesamt-Größe: {total_size:.2f} MB")
    print(f"  Speicherort: {save_dir}")

    print("\n" + "="*70)
    print("  NÄCHSTE SCHRITTE")
    print("="*70)
    print("\n1. Committe den 'models/' Ordner zu Git:")
    print(f"   cd '{Path(__file__).parent}'")
    print("   git add models/")
    print("   git commit -m 'Add pretrained DistilBERT model for offline use'")
    print("   git push")
    print("\n2. In Corporate-Umgebung:")
    print("   git pull")
    print("   python offline_sentiment_analyzer.py")
    print("\n3. Keine Internet-Verbindung zu HuggingFace mehr nötig!")

    return True


def download_tiny_model():
    """
    Alternative: Lädt ein kleineres Model (~25 MB)
    """
    print("="*70)
    print("  KLEINES MODEL DOWNLOAD (Alternative)")
    print("="*70)

    # Verwende ein kleineres distilled Model
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    save_dir = Path(__file__).parent / "models" / "distilbert-small"

    print(f"\nModel: {model_name}")
    print(f"Ziel-Verzeichnis: {save_dir}")
    print("WARNUNG: Nur für Englisch optimiert!")

    # Erstelle Verzeichnis
    save_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1/2] Lade Tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(save_dir)
        print("     ✓ Tokenizer gespeichert")
    except Exception as e:
        print(f"     ✗ Fehler: {e}")
        return False

    print("\n[2/2] Lade Model...")
    try:
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.save_pretrained(save_dir)
        print("     ✓ Model gespeichert")
    except Exception as e:
        print(f"     ✗ Fehler: {e}")
        return False

    total_size = sum(f.stat().st_size for f in save_dir.rglob('*') if f.is_file()) / (1024*1024)
    print(f"\n  Gesamt-Größe: {total_size:.2f} MB")
    print(f"  Speicherort: {save_dir}")

    return True


def create_gitignore():
    """
    Erstellt .gitignore für models/ Ordner (optional)
    """
    gitignore_file = Path(__file__).parent / "models" / ".gitignore"

    # Wenn du die Models NICHT committen willst:
    gitignore_content = """# Uncomment to exclude models from git (not recommended for corporate use)
# *.bin
# pytorch_model.bin

# Keep the folder structure
!.gitignore
"""

    gitignore_file.parent.mkdir(parents=True, exist_ok=True)
    with open(gitignore_file, 'w') as f:
        f.write(gitignore_content)

    print(f"\n✓ .gitignore erstellt in {gitignore_file.parent}")


def main():
    """Hauptfunktion"""
    print("\n" + "="*70)
    print("  MODEL DOWNLOAD für Offline-Verwendung in Corporate-Umgebungen")
    print("="*70)
    print("\nDieses Skript lädt vortrainierte Models herunter und speichert sie")
    print("lokal, sodass sie via Git in Corporate-Umgebungen verwendet werden können.")
    print("\nVoraussetzungen:")
    print("  - Internet-Verbindung (nur beim Download)")
    print("  - pip install transformers torch")

    print("\n" + "="*70)
    print("  WÄHLE MODEL")
    print("="*70)
    print("\n1. DistilBERT Multilingual (~270 MB) - EMPFOHLEN")
    print("   - Hohe Genauigkeit (~93%)")
    print("   - Multi-Language (EN/DE/FR/IT/ES/...)")
    print("   - Produktion-ready")
    print("\n2. DistilBERT Small (~68 MB) - Nur Englisch")
    print("   - Kleinere Größe")
    print("   - Nur für Englisch")
    print("   - Schneller")
    print("\n3. Beide Models")

    choice = input("\nWahl (1/2/3): ").strip()

    success = False

    if choice == "1":
        success = download_distilbert_multilingual()
    elif choice == "2":
        success = download_tiny_model()
    elif choice == "3":
        success = download_distilbert_multilingual()
        if success:
            print("\n" + "="*70)
            success = download_tiny_model()
    else:
        print("Ungültige Wahl!")
        return

    if success:
        # Erstelle .gitignore
        create_gitignore()

        print("\n" + "="*70)
        print("  ✅ ERFOLGREICH!")
        print("="*70)
        print("\nDie Models sind jetzt bereit für Corporate-Deployment via Git.")
        print("\nWICHTIG für Git:")
        print("  - Git LFS empfohlen für große Dateien (>100 MB)")
        print("  - Oder: Verwende Git mit erhöhtem Limit")
        print("  - Alternative: Separate Artifact-Storage (Nexus, Artifactory)")

        print("\nGit LFS Setup (optional, empfohlen):")
        print("  git lfs install")
        print("  git lfs track '*.bin'")
        print("  git add .gitattributes")
        print("  git add models/")
        print("  git commit -m 'Add pretrained models'")
        print("  git push")


if __name__ == "__main__":
    main()
