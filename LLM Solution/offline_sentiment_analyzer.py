"""
Offline Sentiment Analyzer für Corporate-Umgebungen
Verwendet lokal gespeicherte DistilBERT Models - KEINE Internet-Verbindung nötig!
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import json
import logging

# Versuche transformers zu importieren
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("WARNUNG: transformers nicht verfügbar. Fallback auf Lexikon-Modus.")

# Fallback auf Lexikon-Analyzer
try:
    from llm_sentiment_analyzer import LLMSentimentAnalyzer
    LEXICON_AVAILABLE = True
except ImportError:
    LEXICON_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OfflineSentimentAnalyzer:
    """
    Offline Sentiment Analyzer für Corporate-Umgebungen
    Verwendet lokal gespeicherte Models - KEINE HuggingFace-Verbindung nötig
    """

    def __init__(self, model_dir: Optional[str] = None, fallback_to_lexicon: bool = True):
        """
        Initialisiert den Offline Sentiment Analyzer

        Args:
            model_dir: Pfad zum lokal gespeicherten Model
                      (None = automatische Erkennung)
            fallback_to_lexicon: Fallback auf Lexikon wenn Model nicht verfügbar
        """
        self.model = None
        self.tokenizer = None
        self.pipe = None
        self.mode = None
        self.fallback_to_lexicon = fallback_to_lexicon

        # Automatische Model-Erkennung
        if model_dir is None:
            model_dir = self._find_model()

        if model_dir and TRANSFORMERS_AVAILABLE:
            try:
                self._load_offline_model(model_dir)
                self.mode = 'bert'
                logger.info(f"✓ BERT Model geladen (offline) von {model_dir}")
            except Exception as e:
                logger.warning(f"Konnte Model nicht laden: {e}")
                self._setup_fallback()
        else:
            self._setup_fallback()

    def _find_model(self) -> Optional[Path]:
        """Sucht nach lokal gespeichertem Model"""
        base_dir = Path(__file__).parent / "models"

        # Suche nach Model-Verzeichnissen (priorisiert trainierte Models)
        candidates = [
            base_dir / "sentiment-multilingual",  # Trainiert für Sentiment
            base_dir / "distilbert-multilingual",
            base_dir / "distilbert-small",
        ]

        for candidate in candidates:
            if candidate.exists() and (candidate / "config.json").exists():
                logger.info(f"Model gefunden: {candidate}")
                return candidate

        logger.warning("Kein lokales Model gefunden.")
        return None

    def _load_offline_model(self, model_dir: Path):
        """
        Lädt Model komplett offline (keine HuggingFace-Verbindung)

        Args:
            model_dir: Pfad zum Model-Verzeichnis
        """
        logger.info(f"Lade Model von: {model_dir}")

        # Wichtig: local_files_only=True verhindert HuggingFace-Download
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(model_dir),
            local_files_only=True  # ← WICHTIG für Corporate-Umgebungen!
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            str(model_dir),
            local_files_only=True  # ← WICHTIG für Corporate-Umgebungen!
        )

        # Erstelle Pipeline für einfache Verwendung
        self.pipe = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer,
            device=-1  # CPU (verwende 0 für GPU)
        )

        # Lade Metadata wenn vorhanden
        metadata_file = model_dir / "model_info.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                logger.info(f"Model Info: {metadata.get('model_name', 'unknown')}")
                logger.info(f"Languages: {', '.join(metadata.get('languages', []))}")

    def _setup_fallback(self):
        """Setup Fallback auf Lexikon-Modus"""
        if self.fallback_to_lexicon and LEXICON_AVAILABLE:
            logger.info("Verwende Lexikon-Modus (Fallback)")
            self.lexicon_analyzer = LLMSentimentAnalyzer(use_bert=False)
            self.mode = 'lexicon'
        else:
            logger.error("Kein Model verfügbar und Lexikon-Fallback deaktiviert!")
            raise RuntimeError("Kein Sentiment Model verfügbar")

    def analyze(self, text: str) -> Dict:
        """
        Analysiert Text und gibt Sentiment zurück

        Args:
            text: Zu analysierender Text

        Returns:
            Dictionary mit Sentiment-Ergebnis
        """
        if not text or not isinstance(text, str):
            return {
                'score': 0.0,
                'category': 'neutral',
                'confidence': 0.0,
                'mode': self.mode
            }

        if self.mode == 'bert' or self.mode == 'distilbert':
            return self._analyze_with_distilbert(text)
        elif self.mode == 'lexicon':
            return self._analyze_with_lexicon(text)
        else:
            raise RuntimeError("Kein Analyzer verfügbar")

    def _analyze_with_distilbert(self, text: str) -> Dict:
        """Analysiert mit BERT Model (unterstützt 3-class und 5-star Models)"""
        try:
            # Pipeline gibt Label + Score zurück
            result = self.pipe(text[:512])[0]  # Truncate zu max_length

            # Konvertiere zu standardisiertem Format
            label = result['label'].lower()
            confidence = result['score']

            # Label mapping für verschiedene Model-Typen
            if 'star' in label:
                # 5-star rating model (z.B. nlptown)
                if '5 star' in label or '4 star' in label:
                    category = 'positive'
                    score = 0.8 if '5 star' in label else 0.5
                elif '1 star' in label or '2 star' in label:
                    category = 'negative'
                    score = -0.8 if '1 star' in label else -0.5
                else:  # 3 stars
                    category = 'neutral'
                    score = 0.0
            elif 'positive' in label or label == 'label_2':
                category = 'positive'
                score = confidence
            elif 'negative' in label or label == 'label_0':
                category = 'negative'
                score = -confidence
            else:
                category = 'neutral'
                score = 0.0

            return {
                'score': round(score, 3),
                'category': category,
                'confidence': round(confidence, 3),
                'mode': 'bert',
                'raw_label': result['label']
            }

        except Exception as e:
            logger.error(f"DistilBERT Fehler: {e}")
            if self.fallback_to_lexicon:
                logger.info("Fallback auf Lexikon")
                return self._analyze_with_lexicon(text)
            raise

    def _analyze_with_lexicon(self, text: str) -> Dict:
        """Analysiert mit Lexikon (Fallback)"""
        result = self.lexicon_analyzer.analyze(text)
        result['mode'] = 'lexicon'
        return result

    def analyze_batch(self, texts: List[str], batch_size: int = 8) -> List[Dict]:
        """
        Analysiert mehrere Texte

        Args:
            texts: Liste von Texten
            batch_size: Batch-Größe für BERT

        Returns:
            Liste von Sentiment-Ergebnissen
        """
        if self.mode == 'bert' or self.mode == 'distilbert':
            # Batch-Processing mit BERT
            results = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                batch_results = self.pipe(batch)
                results.extend(batch_results)

            # Konvertiere zu standardisiertem Format
            return [self._convert_result(r) for r in results]
        else:
            # Lexikon-Modus
            return [self.analyze(text) for text in texts]

    def _convert_result(self, result: Dict) -> Dict:
        """Konvertiert BERT-Ergebnis zu Standard-Format"""
        label = result['label'].lower()
        confidence = result['score']

        # Label mapping für verschiedene Model-Typen
        if 'star' in label:
            # 5-star rating model
            if '5 star' in label or '4 star' in label:
                category = 'positive'
                score = 0.8 if '5 star' in label else 0.5
            elif '1 star' in label or '2 star' in label:
                category = 'negative'
                score = -0.8 if '1 star' in label else -0.5
            else:  # 3 stars
                category = 'neutral'
                score = 0.0
        elif 'positive' in label or label == 'label_2':
            category = 'positive'
            score = confidence
        elif 'negative' in label or label == 'label_0':
            category = 'negative'
            score = -confidence
        else:
            category = 'neutral'
            score = 0.0

        return {
            'score': round(score, 3),
            'category': category,
            'confidence': round(confidence, 3),
            'mode': 'bert'
        }

    def get_aggregate_sentiment(self, texts: List[str]) -> Dict:
        """Berechnet aggregiertes Sentiment über mehrere Texte"""
        if not texts:
            return {
                'avg_score': 0.0,
                'total_texts': 0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'neutral_ratio': 0.0,
                'mode': self.mode
            }

        results = self.analyze_batch(texts)
        scores = [r['score'] for r in results]
        categories = [r['category'] for r in results]

        return {
            'avg_score': round(sum(scores) / len(scores), 3),
            'median_score': round(sorted(scores)[len(scores) // 2], 3),
            'total_texts': len(texts),
            'positive_ratio': round(categories.count('positive') / len(categories), 3),
            'negative_ratio': round(categories.count('negative') / len(categories), 3),
            'neutral_ratio': round(categories.count('neutral') / len(categories), 3),
            'mode': self.mode
        }

    def get_info(self) -> Dict:
        """Gibt Informationen über den Analyzer zurück"""
        info = {
            'mode': self.mode,
            'transformers_available': TRANSFORMERS_AVAILABLE,
            'lexicon_available': LEXICON_AVAILABLE,
        }

        if self.mode == 'distilbert' and self.model:
            info['model_type'] = self.model.config.model_type
            info['num_labels'] = self.model.config.num_labels

        return info


if __name__ == "__main__":
    # Test
    print("\n" + "="*70)
    print("  OFFLINE SENTIMENT ANALYZER - TEST")
    print("="*70)

    # Initialisiere Analyzer
    print("\nInitialisiere Analyzer...")
    analyzer = OfflineSentimentAnalyzer()

    print(f"\nModus: {analyzer.mode}")
    print(f"Info: {analyzer.get_info()}")

    # Test-Texte (Multi-Language)
    test_texts = [
        ("English", "This is an excellent article! Very helpful and informative."),
        ("English", "This is terrible and completely useless."),
        ("German", "Das ist ein hervorragender Artikel! Sehr hilfreich."),
        ("German", "Das ist schrecklich und völlig unbrauchbar."),
        ("French", "C'est un excellent article! Très utile."),
        ("French", "C'est terrible et complètement inutile."),
        ("Italian", "Questo è un ottimo articolo! Molto utile."),
        ("Italian", "Questo è terribile e completamente inutile."),
    ]

    print("\n" + "="*70)
    print("  EINZELNE ANALYSEN")
    print("="*70)

    for lang, text in test_texts:
        result = analyzer.analyze(text)
        emoji = "😊" if result['score'] > 0 else "😐" if result['score'] == 0 else "😞"

        print(f"\n{emoji} [{lang}] {text}")
        print(f"   Score: {result['score']:+.3f}, Category: {result['category']}, "
              f"Confidence: {result['confidence']:.3f}, Mode: {result['mode']}")

    # Batch-Analyse
    print("\n" + "="*70)
    print("  BATCH-ANALYSE")
    print("="*70)

    comments = [text for _, text in test_texts]
    aggregate = analyzer.get_aggregate_sentiment(comments)

    print(f"\nAnalysierte Texte: {aggregate['total_texts']}")
    print(f"Durchschnittlicher Score: {aggregate['avg_score']:+.3f}")
    print(f"Positive: {aggregate['positive_ratio']:.1%}")
    print(f"Negative: {aggregate['negative_ratio']:.1%}")
    print(f"Neutral: {aggregate['neutral_ratio']:.1%}")
    print(f"Modus: {aggregate['mode']}")

    print("\n" + "="*70)
    print("  TEST ABGESCHLOSSEN")
    print("="*70)
