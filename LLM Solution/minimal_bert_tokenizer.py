"""
Minimale BERT Tokenizer Implementierung
Ohne externe Dependencies - nur Python Standard Library
"""

import json
import re
from typing import List, Dict, Tuple


class MinimalBertTokenizer:
    """
    Vereinfachte BERT Tokenizer Implementierung
    Basiert auf WordPiece Tokenization
    """

    def __init__(self, vocab_file: str = None):
        """Initialisiert den Tokenizer"""
        self.vocab = {}
        self.ids_to_tokens = {}
        self.max_input_chars_per_word = 100

        # Special tokens
        self.pad_token = "[PAD]"
        self.unk_token = "[UNK]"
        self.cls_token = "[CLS]"
        self.sep_token = "[SEP]"
        self.mask_token = "[MASK]"

        self.pad_token_id = 0
        self.unk_token_id = 100
        self.cls_token_id = 101
        self.sep_token_id = 102
        self.mask_token_id = 103

        # Wenn vocab_file gegeben, lade es
        if vocab_file:
            self.load_vocab(vocab_file)
        else:
            # Erstelle minimales deutsches Vocab
            self._create_minimal_german_vocab()

    def _create_minimal_german_vocab(self):
        """Erstellt ein minimales deutsches Vokabular für Sentiment-Analyse"""

        # Special tokens
        special_tokens = [
            "[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"
        ]

        # Häufige deutsche Wörter und Sentiment-relevante Tokens
        german_tokens = [
            # Artikel, Pronomen
            "der", "die", "das", "den", "dem", "des", "ein", "eine", "einer", "einen",
            "ich", "du", "er", "sie", "es", "wir", "ihr", "man",

            # Häufige Verben
            "ist", "sind", "war", "waren", "sein", "haben", "hat", "hatte",
            "kann", "könnte", "muss", "soll", "will", "würde",
            "macht", "sagt", "gibt", "kommt", "geht",

            # Sentiment positiv
            "gut", "super", "toll", "exzellent", "hervorragend", "großartig",
            "prima", "perfekt", "genial", "wunderbar", "fantastisch",
            "hilfreich", "nützlich", "wertvoll", "wichtig", "interessant",
            "klar", "verständlich", "deutlich", "transparent",
            "freude", "freuen", "gefallen", "mögen", "lieben",
            "richtig", "korrekt", "passend", "empfehlen",

            # Sentiment negativ
            "schlecht", "schrecklich", "furchtbar", "katastrophal",
            "unnütz", "nutzlos", "wertlos", "langweilig",
            "unklar", "unverständlich", "verwirrend", "chaotisch",
            "ärger", "enttäuscht", "frustration", "verärgert",
            "problem", "fehler", "mangel", "schwäche",
            "falsch", "inkorrekt", "ablehnen",

            # Verstärker
            "sehr", "extrem", "besonders", "äußerst", "total",
            "wirklich", "echt", "ziemlich",

            # Negationen
            "nicht", "kein", "keine", "niemals", "nie", "ohne",

            # Konjunktionen
            "und", "oder", "aber", "doch", "wenn", "als", "wie",
            "dass", "weil", "da", "obwohl",

            # Satzzeichen
            ".", ",", "!", "?", ":", ";", "-",
        ]

        # Erstelle Vocab
        all_tokens = special_tokens + german_tokens

        # Füge auch Subword-Varianten hinzu (##prefix)
        subwords = []
        for token in german_tokens[10:]:  # Nur für längere Wörter
            if len(token) > 3:
                for i in range(2, len(token)):
                    subwords.append(f"##{token[i:]}")

        all_tokens.extend(subwords[:200])  # Limitiere Subwords

        # Erstelle Vocab Dictionary
        self.vocab = {token: idx for idx, token in enumerate(all_tokens)}
        self.ids_to_tokens = {idx: token for token, idx in self.vocab.items()}

        # Update special token IDs
        self.pad_token_id = self.vocab.get("[PAD]", 0)
        self.unk_token_id = self.vocab.get("[UNK]", 1)
        self.cls_token_id = self.vocab.get("[CLS]", 2)
        self.sep_token_id = self.vocab.get("[SEP]", 3)
        self.mask_token_id = self.vocab.get("[MASK]", 4)

    def load_vocab(self, vocab_file: str):
        """Lädt Vokabular aus Datei"""
        try:
            with open(vocab_file, 'r', encoding='utf-8') as f:
                if vocab_file.endswith('.json'):
                    self.vocab = json.load(f)
                else:
                    # txt Format (ein Token pro Zeile)
                    tokens = [line.strip() for line in f]
                    self.vocab = {token: idx for idx, token in enumerate(tokens)}

            self.ids_to_tokens = {idx: token for token, idx in self.vocab.items()}
        except Exception as e:
            print(f"Warnung: Konnte Vocab nicht laden: {e}")
            self._create_minimal_german_vocab()

    def basic_tokenize(self, text: str) -> List[str]:
        """Basis-Tokenisierung (Whitespace + Interpunktion)"""
        # Kleinbuchstaben
        text = text.lower()

        # Füge Leerzeichen um Satzzeichen hinzu
        text = re.sub(r'([.,!?;:\-])', r' \1 ', text)

        # Entferne mehrfache Leerzeichen
        text = re.sub(r'\s+', ' ', text).strip()

        # Splitte
        tokens = text.split()

        return tokens

    def wordpiece_tokenize(self, word: str) -> List[str]:
        """WordPiece Tokenisierung eines Wortes"""
        if len(word) > self.max_input_chars_per_word:
            return [self.unk_token]

        # Wenn Wort im Vocab, return es
        if word in self.vocab:
            return [word]

        # Ansonsten zerlege in Subwords
        tokens = []
        start = 0

        while start < len(word):
            end = len(word)
            cur_substr = None

            # Finde längstes Subword
            while start < end:
                substr = word[start:end]
                if start > 0:
                    substr = "##" + substr

                if substr in self.vocab:
                    cur_substr = substr
                    break
                end -= 1

            if cur_substr is None:
                tokens.append(self.unk_token)
                break

            tokens.append(cur_substr)
            start = end

        return tokens

    def tokenize(self, text: str) -> List[str]:
        """Tokenisiert Text"""
        # Basis-Tokenisierung
        words = self.basic_tokenize(text)

        # WordPiece Tokenisierung
        tokens = []
        for word in words:
            tokens.extend(self.wordpiece_tokenize(word))

        return tokens

    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        """Konvertiert Tokens zu IDs"""
        return [self.vocab.get(token, self.unk_token_id) for token in tokens]

    def encode(self, text: str, max_length: int = 512,
               add_special_tokens: bool = True,
               padding: str = 'max_length',
               truncation: bool = True) -> Dict[str, List[int]]:
        """
        Encodiert Text zu Input IDs

        Args:
            text: Eingabe-Text
            max_length: Maximale Länge
            add_special_tokens: Füge [CLS] und [SEP] hinzu
            padding: Padding-Strategie
            truncation: Truncate wenn zu lang

        Returns:
            Dictionary mit input_ids und attention_mask
        """
        # Tokenisiere
        tokens = self.tokenize(text)

        # Füge special tokens hinzu
        if add_special_tokens:
            tokens = [self.cls_token] + tokens + [self.sep_token]

        # Truncate
        if truncation and len(tokens) > max_length:
            tokens = tokens[:max_length-1] + [self.sep_token]

        # Konvertiere zu IDs
        input_ids = self.convert_tokens_to_ids(tokens)

        # Attention mask (1 für echte Tokens, 0 für Padding)
        attention_mask = [1] * len(input_ids)

        # Padding
        if padding == 'max_length':
            padding_length = max_length - len(input_ids)
            input_ids = input_ids + [self.pad_token_id] * padding_length
            attention_mask = attention_mask + [0] * padding_length

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask
        }

    def decode(self, ids: List[int]) -> str:
        """Dekodiert IDs zurück zu Text"""
        tokens = [self.ids_to_tokens.get(id, self.unk_token) for id in ids]

        # Entferne special tokens
        tokens = [t for t in tokens if t not in [self.pad_token, self.cls_token,
                                                  self.sep_token, self.mask_token]]

        # Merge Subwords
        text = " ".join(tokens)
        text = text.replace(" ##", "")

        return text


if __name__ == "__main__":
    # Test
    tokenizer = MinimalBertTokenizer()

    test_texts = [
        "Das ist ein sehr guter Artikel!",
        "Leider schlecht erklärt und unverständlich.",
        "Super hilfreich und klar strukturiert.",
    ]

    for text in test_texts:
        print(f"\nText: {text}")
        tokens = tokenizer.tokenize(text)
        print(f"Tokens: {tokens}")

        encoded = tokenizer.encode(text, max_length=32)
        print(f"Input IDs: {encoded['input_ids'][:10]}...")
        print(f"Attention Mask: {encoded['attention_mask'][:10]}...")
