#!/bin/bash

# Installation Script für macOS/Linux

echo "==================================="
echo "Sentiment Analysis - Installation"
echo "==================================="

# Prüfe Python-Version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python Version: $python_version"

# Erstelle virtuelle Umgebung
echo ""
echo "Erstelle virtuelle Umgebung..."
python3 -m venv venv

# Aktiviere virtuelle Umgebung
echo "Aktiviere virtuelle Umgebung..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrade pip..."
pip install --upgrade pip

# Installiere Dependencies
echo ""
echo "Installiere Dependencies..."
pip install -r requirements.txt

# Download NLTK Daten (optional)
echo ""
echo "Lade NLTK Daten (optional, für VADER)..."
python3 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')" 2>/dev/null || echo "NLTK installation übersprungen"

echo ""
echo "==================================="
echo "Installation abgeschlossen!"
echo "==================================="
echo ""
echo "Nächste Schritte:"
echo "1. Aktiviere die virtuelle Umgebung: source venv/bin/activate"
echo "2. Lege deine Excel-Datei in data/input/ ab"
echo "3. Führe aus: python main.py --input data/input/deine_datei.xlsx"
echo ""
