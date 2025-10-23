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
