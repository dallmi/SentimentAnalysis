"""
LLM-basierter Sentiment Analyzer mit Multi-Language Support
Verwendet Minimal-BERT Implementierung
Unterstützt: Englisch, Deutsch, Französisch, Italienisch
"""

import numpy as np
from typing import Dict, List, Optional
import logging
from minimal_bert_tokenizer import MinimalBertTokenizer
from minimal_bert_model import MinimalBertForSentiment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultilingualSentimentLexicon:
    """
    Multilinguales Sentiment-Lexikon
    Fallback wenn BERT Model nicht verfügbar
    """

    def __init__(self):
        """Initialisiert das multilunguale Lexikon"""
        self.positive_words = self._load_positive_lexicon()
        self.negative_words = self._load_negative_lexicon()
        self.intensifiers = self._load_intensifiers()
        self.negations = self._load_negations()

        logger.info(f"Multilingual Lexicon loaded: {len(self.positive_words)} positive, "
                   f"{len(self.negative_words)} negative words")

    def _load_positive_lexicon(self) -> set:
        """Lädt positive Wörter für alle Sprachen"""
        return {
            # English
            'good', 'great', 'excellent', 'awesome', 'fantastic', 'wonderful',
            'perfect', 'amazing', 'brilliant', 'outstanding', 'superb',
            'helpful', 'useful', 'valuable', 'important', 'interesting',
            'clear', 'understandable', 'transparent', 'informative',
            'happy', 'pleased', 'satisfied', 'love', 'like', 'enjoy',
            'recommend', 'support', 'appreciate', 'thank', 'thanks',
            'better', 'best', 'improved', 'improvement', 'positive',

            # German
            'gut', 'super', 'toll', 'exzellent', 'hervorragend', 'ausgezeichnet',
            'fantastisch', 'großartig', 'wunderbar', 'prima', 'perfekt',
            'hilfreich', 'nützlich', 'wertvoll', 'wichtig', 'interessant',
            'klar', 'verständlich', 'deutlich', 'transparent', 'informativ',
            'freuen', 'freude', 'gefallen', 'mögen', 'lieben', 'zufrieden',
            'empfehlen', 'unterstützen', 'danke', 'besser', 'positiv',

            # French
            'bon', 'bien', 'excellent', 'formidable', 'magnifique', 'super',
            'parfait', 'génial', 'merveilleux', 'fantastique', 'incroyable',
            'utile', 'précieux', 'important', 'intéressant', 'clair',
            'heureux', 'content', 'satisfait', 'aimer', 'adorer',
            'recommander', 'remercier', 'merci', 'meilleur', 'positif',

            # Italian
            'buono', 'ottimo', 'eccellente', 'fantastico', 'magnifico', 'super',
            'perfetto', 'meraviglioso', 'brillante', 'straordinario',
            'utile', 'prezioso', 'importante', 'interessante', 'chiaro',
            'felice', 'contento', 'soddisfatto', 'amare', 'piacere',
            'raccomandare', 'grazie', 'migliore', 'positivo',
        }

    def _load_negative_lexicon(self) -> set:
        """Lädt negative Wörter für alle Sprachen"""
        return {
            # English
            'bad', 'terrible', 'horrible', 'awful', 'poor', 'worst',
            'useless', 'worthless', 'disappointing', 'disappointed',
            'unclear', 'confusing', 'complicated', 'difficult',
            'unhappy', 'unsatisfied', 'frustrated', 'angry', 'hate',
            'problem', 'error', 'issue', 'wrong', 'incorrect', 'fail',
            'worse', 'negative', 'unfortunately', 'sadly',

            # German
            'schlecht', 'schrecklich', 'furchtbar', 'katastrophal',
            'unnütz', 'nutzlos', 'wertlos', 'enttäuschend', 'enttäuscht',
            'unklar', 'verwirrend', 'kompliziert', 'schwierig',
            'unglücklich', 'unzufrieden', 'frustriert', 'verärgert',
            'problem', 'fehler', 'falsch', 'inkorrekt', 'versagen',
            'schlechter', 'negativ', 'leider',

            # French
            'mauvais', 'terrible', 'horrible', 'affreux', 'pire',
            'inutile', 'décevant', 'déçu', 'confus', 'compliqué',
            'malheureux', 'insatisfait', 'frustré', 'problème',
            'erreur', 'faux', 'incorrect', 'échec', 'négatif',
            'malheureusement', 'dommage',

            # Italian
            'cattivo', 'terribile', 'orribile', 'pessimo', 'peggiore',
            'inutile', 'deludente', 'deluso', 'confuso', 'complicato',
            'infelice', 'insoddisfatto', 'frustrato', 'problema',
            'errore', 'sbagliato', 'incorrecto', 'fallire', 'negativo',
            'purtroppo', 'sfortunatamente',
        }

    def _load_intensifiers(self) -> set:
        """Lädt Verstärker für alle Sprachen"""
        return {
            # English
            'very', 'extremely', 'really', 'absolutely', 'totally',
            'completely', 'highly', 'particularly',

            # German
            'sehr', 'extrem', 'besonders', 'äußerst', 'total',
            'absolut', 'völlig', 'wirklich', 'echt',

            # French
            'très', 'extrêmement', 'vraiment', 'absolument', 'totalement',
            'complètement', 'particulièrement',

            # Italian
            'molto', 'estremamente', 'veramente', 'assolutamente',
            'totalmente', 'completamente', 'particolarmente',
        }

    def _load_negations(self) -> set:
        """Lädt Negationen für alle Sprachen"""
        return {
            # English
            'not', 'no', 'never', 'none', 'nothing', 'nobody',
            'neither', 'nor', 'without', "don't", "doesn't", "didn't",
            "won't", "wouldn't", "can't", "couldn't", "shouldn't",

            # German
            'nicht', 'kein', 'keine', 'keinen', 'niemals', 'nie',
            'nichts', 'niemand', 'weder', 'ohne',

            # French
            'pas', 'non', 'jamais', 'aucun', 'rien', 'personne',
            'ni', 'sans',

            # Italian
            'non', 'no', 'mai', 'nessuno', 'niente', 'né', 'senza',
        }


class LLMSentimentAnalyzer:
    """
    LLM-basierter Sentiment Analyzer
    Verwendet Mini-BERT oder Fallback auf Lexikon
    """

    def __init__(self, use_bert: bool = True, model_path: Optional[str] = None):
        """
        Initialisiert den LLM Sentiment Analyzer

        Args:
            use_bert: Verwende BERT Model wenn True, sonst Lexikon
            model_path: Pfad zu vortrainierten BERT Gewichten
        """
        self.use_bert = use_bert
        self.lexicon = MultilingualSentimentLexicon()

        if use_bert:
            try:
                logger.info("Initialisiere Mini-BERT Model...")
                self.tokenizer = MinimalBertTokenizer()

                if model_path:
                    self.model = MinimalBertForSentiment.load(model_path)
                    logger.info(f"BERT Model geladen von: {model_path}")
                else:
                    self.model = MinimalBertForSentiment(
                        vocab_size=len(self.tokenizer.vocab),
                        hidden_size=128,
                        num_hidden_layers=2,
                        num_attention_heads=4,
                        num_labels=3
                    )
                    logger.info("BERT Model mit Default-Gewichten initialisiert")

            except Exception as e:
                logger.warning(f"Konnte BERT nicht initialisieren: {e}")
                logger.info("Fallback auf Lexikon-basierte Analyse")
                self.use_bert = False

    def analyze_with_bert(self, text: str) -> Dict:
        """
        Analysiert Text mit BERT Model

        Args:
            text: Zu analysierender Text

        Returns:
            Sentiment-Ergebnis
        """
        # Tokenize
        encoded = self.tokenizer.encode(text, max_length=128)

        # Konvertiere zu numpy arrays
        input_ids = np.array([encoded['input_ids']])
        attention_mask = np.array([encoded['attention_mask']])

        # Predict
        results = self.model.predict(input_ids, attention_mask)
        result = results[0]

        # Konvertiere zu standardisiertem Format
        # Label mapping: negative=-1, neutral=0, positive=1
        label_to_score = {
            'negative': -0.8,
            'neutral': 0.0,
            'positive': 0.8
        }

        score = label_to_score[result['label']]

        return {
            'score': score,
            'category': result['label'],
            'confidence': result['score'],
            'method': 'bert',
            'all_scores': result['all_scores']
        }

    def analyze_with_lexicon(self, text: str) -> Dict:
        """
        Analysiert Text mit Lexikon

        Args:
            text: Zu analysierender Text

        Returns:
            Sentiment-Ergebnis
        """
        # Tokenize
        tokens = text.lower().split()

        positive_count = 0
        negative_count = 0
        intensity_multiplier = 1.0
        negation_active = False

        for token in tokens:
            # Check negation
            if token in self.lexicon.negations:
                negation_active = True
                continue

            # Check intensifier
            if token in self.lexicon.intensifiers:
                intensity_multiplier = 1.5
                continue

            # Check sentiment
            if token in self.lexicon.positive_words:
                score = intensity_multiplier
                if negation_active:
                    negative_count += score
                else:
                    positive_count += score

            elif token in self.lexicon.negative_words:
                score = intensity_multiplier
                if negation_active:
                    positive_count += score
                else:
                    negative_count += score

            # Reset
            intensity_multiplier = 1.0
            negation_active = False

        # Calculate score
        total = positive_count + negative_count
        if total == 0:
            score = 0.0
            confidence = 0.0
        else:
            score = (positive_count - negative_count) / total
            confidence = min(total / len(tokens), 1.0)

        # Categorize
        if score > 0.3:
            category = 'positive'
        elif score < -0.3:
            category = 'negative'
        else:
            category = 'neutral'

        return {
            'score': round(score, 3),
            'category': category,
            'confidence': round(confidence, 3),
            'method': 'lexicon',
            'positive_count': round(positive_count, 2),
            'negative_count': round(negative_count, 2)
        }

    def analyze(self, text: str) -> Dict:
        """
        Analysiert Text (verwendet BERT oder Lexikon)

        Args:
            text: Zu analysierender Text

        Returns:
            Sentiment-Ergebnis
        """
        if not text or not isinstance(text, str):
            return {
                'score': 0.0,
                'category': 'neutral',
                'confidence': 0.0,
                'method': 'none'
            }

        if self.use_bert:
            try:
                return self.analyze_with_bert(text)
            except Exception as e:
                logger.warning(f"BERT Analyse fehlgeschlagen: {e}, Fallback auf Lexikon")
                return self.analyze_with_lexicon(text)
        else:
            return self.analyze_with_lexicon(text)

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analysiert mehrere Texte

        Args:
            texts: Liste von Texten

        Returns:
            Liste von Sentiment-Ergebnissen
        """
        return [self.analyze(text) for text in texts]

    def get_aggregate_sentiment(self, texts: List[str]) -> Dict:
        """
        Berechnet aggregiertes Sentiment

        Args:
            texts: Liste von Texten

        Returns:
            Aggregiertes Sentiment
        """
        if not texts:
            return {
                'avg_score': 0.0,
                'total_texts': 0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'neutral_ratio': 0.0
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
            'method': results[0]['method'] if results else 'none'
        }


if __name__ == "__main__":
    # Test
    print("Initialisiere LLM Sentiment Analyzer...")
    analyzer = LLMSentimentAnalyzer(use_bert=True)

    # Multilingual test texts
    test_texts = [
        # English
        "This is a very good article! Super helpful and informative.",
        "Unfortunately very poorly explained and unclear.",

        # German
        "Das ist ein hervorragender Artikel! Sehr hilfreich.",
        "Leider sehr schlecht erklärt und verwirrend.",

        # French
        "C'est un excellent article! Très utile et clair.",
        "Malheureusement très mal expliqué et confus.",

        # Italian
        "Questo è un ottimo articolo! Molto utile e chiaro.",
        "Purtroppo molto mal spiegato e confuso.",
    ]

    print("\n" + "="*60)
    print("MULTILINGUAL SENTIMENT ANALYSIS")
    print("="*60)

    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\nText: {text}")
        print(f"  Score: {result['score']:+.3f}")
        print(f"  Category: {result['category']}")
        print(f"  Confidence: {result['confidence']:.3f}")
        print(f"  Method: {result['method']}")

    # Batch analysis
    print("\n" + "="*60)
    print("AGGREGATE SENTIMENT")
    print("="*60)
    aggregate = analyzer.get_aggregate_sentiment(test_texts)
    print(f"Average Score: {aggregate['avg_score']:+.3f}")
    print(f"Positive Ratio: {aggregate['positive_ratio']:.1%}")
    print(f"Negative Ratio: {aggregate['negative_ratio']:.1%}")
    print(f"Neutral Ratio: {aggregate['neutral_ratio']:.1%}")
