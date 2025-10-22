#!/bin/bash

# Quick Start Script

echo "Sentiment Analysis - Quick Start"
echo "================================="

# Aktiviere virtuelle Umgebung falls vorhanden
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtuelle Umgebung aktiviert"
else
    echo "⚠ Keine virtuelle Umgebung gefunden. Führe erst ./install.sh aus!"
    exit 1
fi

# Suche nach Excel-Dateien
echo ""
echo "Suche nach Excel-Dateien in data/input/..."
input_files=$(find data/input -name "*.xlsx" -o -name "*.xls" 2>/dev/null)

if [ -z "$input_files" ]; then
    echo "⚠ Keine Excel-Dateien in data/input/ gefunden!"
    echo "Bitte lege eine Excel-Datei dort ab."
    exit 1
fi

# Zeige gefundene Dateien
echo "Gefundene Dateien:"
echo "$input_files"

# Verwende die neueste Datei
latest_file=$(ls -t data/input/*.xlsx data/input/*.xls 2>/dev/null | head -1)
echo ""
echo "Verwende: $latest_file"
echo ""

# Frage nach Optionen
read -p "Mit VADER Sentiment Analyzer? (j/N): " use_vader
read -p "Web Scraping überspringen? (j/N): " no_scraping

# Baue Befehl
cmd="python main.py --input \"$latest_file\""

if [[ $use_vader == "j" || $use_vader == "J" ]]; then
    cmd="$cmd --use-vader"
fi

if [[ $no_scraping == "j" || $no_scraping == "J" ]]; then
    cmd="$cmd --no-scraping"
fi

echo ""
echo "Führe aus: $cmd"
echo ""

# Führe aus
eval $cmd

echo ""
echo "Fertig! Prüfe data/output/ für die Ergebnisse."
