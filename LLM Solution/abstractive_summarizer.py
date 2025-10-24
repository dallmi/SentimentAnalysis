"""
Abstractive Summarization using mBART-large-50
Generates new summary text (not just extracting sentences)

Supports 50+ languages including German, English, French, Italian, Spanish
"""

import torch
from transformers import MBartForConditionalGeneration, MBart50Tokenizer
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class AbstractiveSummarizer:
    """
    Abstractive summarization using mBART-large-50.
    Generates new, concise summary text from articles.
    """

    def __init__(self, model_path: str = None):
        """
        Initialize abstractive summarizer.

        Args:
            model_path: Path to local mBART model directory
        """
        if model_path is None:
            # Default path
            base_dir = Path(__file__).parent
            model_path = base_dir / "models" / "mbart-large-50"

        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {self.model_path}\n"
                "Download with: python setup/download_mbart_model.py"
            )

        logger.info(f"Loading mBART model from {self.model_path}...")

        # Load tokenizer and model
        self.tokenizer = MBart50Tokenizer.from_pretrained(str(self.model_path))
        self.model = MBartForConditionalGeneration.from_pretrained(str(self.model_path))

        # Set device (GPU if available)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

        logger.info(f"   ✓ Model loaded on {self.device}")

    def summarize(
        self,
        text: str,
        source_lang: str = "de_DE",
        max_length: int = 150,
        min_length: int = 40,
        num_beams: int = 4,
        length_penalty: float = 2.0,
        early_stopping: bool = True
    ) -> str:
        """
        Generate abstractive summary of text.

        Args:
            text: Text to summarize
            source_lang: Source language code (de_DE, en_XX, fr_XX, etc.)
            max_length: Maximum summary length in tokens
            min_length: Minimum summary length in tokens
            num_beams: Number of beams for beam search
            length_penalty: Length penalty (>1.0 favors longer summaries)
            early_stopping: Stop when num_beams sentences are done

        Returns:
            Generated summary text
        """
        if not text or not text.strip():
            return ""

        # Truncate input if too long (mBART has 1024 token limit)
        max_input_tokens = 1024
        inputs = self.tokenizer(
            text,
            max_length=max_input_tokens,
            truncation=True,
            return_tensors="pt"
        )
        inputs = inputs.to(self.device)

        # Set source language
        self.tokenizer.src_lang = source_lang

        # Generate summary
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            num_beams=num_beams,
            length_penalty=length_penalty,
            early_stopping=early_stopping,
            forced_bos_token_id=self.tokenizer.lang_code_to_id[source_lang]
        )

        # Decode summary
        summary = self.tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )

        return summary.strip()

    def summarize_batch(
        self,
        texts: list,
        source_lang: str = "de_DE",
        **kwargs
    ) -> list:
        """
        Summarize multiple texts in batch.

        Args:
            texts: List of texts to summarize
            source_lang: Source language code
            **kwargs: Additional arguments for summarize()

        Returns:
            List of summaries
        """
        summaries = []
        for text in texts:
            summary = self.summarize(text, source_lang=source_lang, **kwargs)
            summaries.append(summary)
        return summaries

    def generate_topic_label(
        self,
        keywords: list,
        representative_docs: list,
        source_lang: str = "de_DE",
        max_keywords: int = 3
    ) -> str:
        """
        Generate concise topic label (1-3 keywords) from topic keywords and documents.

        Args:
            keywords: List of (word, score) tuples from BERTopic
            representative_docs: List of representative documents for this topic
            source_lang: Source language code
            max_keywords: Maximum number of keywords to return (1-3)

        Returns:
            Concise topic label (e.g., "Homeoffice", "KI & Automatisierung", "Nachhaltigkeit")
        """
        print("\n🔍 INSIDE generate_topic_label()...")
        print(f"   Keywords: {keywords[:3] if keywords else 'None'}")
        print(f"   Docs: {len(representative_docs) if representative_docs else 0}")
        print(f"   source_lang: {source_lang}")
        print(f"   max_keywords: {max_keywords}")

        if not keywords and not representative_docs:
            print("   → Returning 'Sonstiges' (no keywords/docs)")
            return "Sonstiges"

        # Define stopwords FIRST (before using them)
        stopwords = {
            # English stopwords
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were',
            'our', 'my', 'your', 'their', 'his', 'her',
            'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'it', 'its',
            # German stopwords (safety - shouldn't occur with forced English output)
            'der', 'die', 'das', 'den', 'dem', 'des',
            'ein', 'eine', 'einen', 'einem', 'einer',
            'und', 'oder', 'aber', 'als', 'auch',
            'bei', 'von', 'zu', 'mit', 'nach', 'für',
            'auf', 'um', 'durch', 'über',
            'es', 'sich', 'wird', 'werden',
            # Company-specific
            'ubs'
        }

        # Filter stopwords from BERTopic keywords BEFORE sending to mBART
        # This prevents mBART from seeing stopwords in the input
        filtered_keywords = [(word, score) for word, score in keywords if word.lower() not in stopwords]

        # If all keywords were stopwords, use original keywords (fallback)
        if not filtered_keywords:
            print("   ⚠️  All keywords were stopwords! Using original keywords.")
            filtered_keywords = keywords

        # Take top 5 filtered keywords
        top_keywords = [word for word, _ in filtered_keywords[:5]]
        keyword_text = ", ".join(top_keywords)

        print(f"   Filtered keywords (stopwords removed): {top_keywords}")

        # Simple prompt - keywords can be in any language (German, English, etc.)
        # Always request English output for consistency
        prompt = f"Keywords: {keyword_text}\n\nTopic label in English (1-3 words):"

        # Generate with mBART (shorter output for keywords)
        inputs = self.tokenizer(
            prompt,
            max_length=256,  # Shorter input
            truncation=True,
            return_tensors="pt"
        )
        inputs = inputs.to(self.device)

        # IMPORTANT: Accept input in source_lang (could be de_DE, en_XX, etc.)
        # But FORCE output to English via forced_bos_token_id
        self.tokenizer.src_lang = source_lang  # Accept any input language

        # Generate very short label (max 10 tokens for 1-3 keywords)
        # mBART-large-50 supports 50+ languages for BOTH input and output
        # We accept German/English/etc keywords as input (via source_lang)
        # But ALWAYS generate English output (via forced_bos_token_id)
        label_ids = self.model.generate(
            inputs["input_ids"],
            max_length=10,  # Much shorter - only 1-3 words
            min_length=1,
            num_beams=4,
            length_penalty=0.3,  # Strongly favor shorter outputs
            early_stopping=True,
            forced_bos_token_id=self.tokenizer.lang_code_to_id["en_XX"],  # ALWAYS output English
            no_repeat_ngram_size=2,
            repetition_penalty=2.0  # Avoid repetition
        )

        # Decode label
        label = self.tokenizer.decode(
            label_ids[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )

        # Clean up: Remove punctuation at the end
        raw_label = label.strip().rstrip('.,!?;:')

        # Filter out stopwords from mBART output (reuse stopwords defined earlier)
        # This catches any stopwords that mBART generated despite our input filtering
        words = raw_label.split()
        filtered_words = [w for w in words if w.lower() not in stopwords]

        # If filtering removed everything, keep original
        if filtered_words:
            label = ' '.join(filtered_words)
        else:
            label = raw_label

        # Capitalize each word for consistency (Title Case)
        label = ' '.join(word.capitalize() for word in label.split())

        # Show before/after if stopwords were removed
        print(f"   Raw mBART output: '{raw_label}'")
        if raw_label != label:
            print(f"   After stopword removal: '{label}'")
        print(f"   Word count: {len(label.split())}")
        print(f"   Max allowed words: {max_keywords + 1}")

        # Fallback: If mBART generates too long or empty, use top keywords
        if not label:
            print(f"   ⚠️  Fallback triggered! Output is EMPTY")
            # Use top keywords as fallback
            top_words = [word.capitalize() for word, _ in keywords[:max_keywords]]
            label = " & ".join(top_words) if top_words else "Sonstiges"
            print(f"   → Fallback label: '{label}'")
        elif len(label.split()) > max_keywords + 1:
            print(f"   ⚠️  Fallback triggered! Output too long ({len(label.split())} words > {max_keywords + 1})")
            print(f"   → Too long output was: '{label}'")
            # Use top keywords as fallback
            top_words = [word.capitalize() for word, _ in keywords[:max_keywords]]
            label = " & ".join(top_words) if top_words else "Sonstiges"
            print(f"   → Fallback label: '{label}'")

        return label


# Language code mapping for common languages
LANGUAGE_CODES = {
    "german": "de_DE",
    "deutsch": "de_DE",
    "de": "de_DE",
    "english": "en_XX",
    "en": "en_XX",
    "french": "fr_XX",
    "français": "fr_XX",
    "fr": "fr_XX",
    "italian": "it_IT",
    "italiano": "it_IT",
    "it": "it_IT",
    "spanish": "es_XX",
    "español": "es_XX",
    "es": "es_XX",
}


def get_language_code(language: str) -> str:
    """
    Get mBART language code from language name.

    Args:
        language: Language name (e.g., "german", "de", "english")

    Returns:
        mBART language code (e.g., "de_DE", "en_XX")
    """
    language = language.lower().strip()
    return LANGUAGE_CODES.get(language, "de_DE")  # Default to German


if __name__ == "__main__":
    # Test with sample German text
    print("Testing abstractive summarization...")

    try:
        summarizer = AbstractiveSummarizer()

        test_text = """
        Die Geschäftsführung hat eine neue Richtlinie für flexibles Arbeiten verabschiedet.
        Ab dem 1. Januar 2025 können alle Mitarbeiter bis zu drei Tage pro Woche von zu Hause arbeiten.
        Diese Entscheidung wurde nach umfangreichen Mitarbeiterbefragungen getroffen, bei denen
        sich eine klare Mehrheit für mehr Flexibilität ausgesprochen hat. Die IT-Abteilung stellt
        die notwendige Hardware und Software zur Verfügung. Für die Nutzung ist ein Antrag über
        das HR-Portal erforderlich. Führungskräfte müssen die Anträge innerhalb von fünf
        Arbeitstagen prüfen. Die neue Regelung gilt für alle Abteilungen außer dem Kundenservice.
        Mitarbeiter im Kundenservice haben spezielle Schichtpläne und sind davon ausgenommen.
        """

        print("\nOriginal text:")
        print(test_text.strip())
        print("\n" + "=" * 70)

        summary = summarizer.summarize(test_text, source_lang="de_DE", max_length=100)

        print("\nAbstractive summary:")
        print(summary)
        print("\n" + "=" * 70)
        print("✓ Test successful!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure to download the model first:")
        print("  python setup/download_mbart_model.py")
