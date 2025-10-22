"""
Minimale BERT Model Implementierung für Sentiment Classification
Nur mit NumPy - keine ML-Framework Dependencies
"""

import json
import pickle
import numpy as np
from typing import Dict, List, Tuple, Optional
import os


class MinimalBertEmbedding:
    """Token + Position + Segment Embeddings"""

    def __init__(self, vocab_size: int = 500, hidden_size: int = 128,
                 max_position_embeddings: int = 512):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.max_position_embeddings = max_position_embeddings

        # Initialisiere Embedding Matrizen (zufällig)
        np.random.seed(42)
        self.token_embeddings = np.random.randn(vocab_size, hidden_size) * 0.02
        self.position_embeddings = np.random.randn(max_position_embeddings, hidden_size) * 0.02
        self.token_type_embeddings = np.random.randn(2, hidden_size) * 0.02

        # LayerNorm Parameter
        self.gamma = np.ones(hidden_size)
        self.beta = np.zeros(hidden_size)

    def forward(self, input_ids: np.ndarray, token_type_ids: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Forward pass durch Embeddings

        Args:
            input_ids: [batch_size, seq_length]
            token_type_ids: [batch_size, seq_length]

        Returns:
            embeddings: [batch_size, seq_length, hidden_size]
        """
        batch_size, seq_length = input_ids.shape

        # Token embeddings
        token_embeds = self.token_embeddings[input_ids]  # [batch, seq, hidden]

        # Position embeddings
        position_ids = np.arange(seq_length)
        position_embeds = self.position_embeddings[position_ids]  # [seq, hidden]
        position_embeds = np.expand_dims(position_embeds, 0)  # [1, seq, hidden]

        # Segment embeddings
        if token_type_ids is None:
            token_type_ids = np.zeros_like(input_ids)
        segment_embeds = self.token_type_embeddings[token_type_ids]

        # Addiere alle Embeddings
        embeddings = token_embeds + position_embeds + segment_embeds

        # LayerNorm
        embeddings = self.layer_norm(embeddings)

        return embeddings

    def layer_norm(self, x: np.ndarray, epsilon: float = 1e-12) -> np.ndarray:
        """Layer Normalization"""
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return self.gamma * (x - mean) / (std + epsilon) + self.beta


class MinimalBertSelfAttention:
    """Simplified Self-Attention Layer"""

    def __init__(self, hidden_size: int = 128, num_attention_heads: int = 4):
        self.hidden_size = hidden_size
        self.num_attention_heads = num_attention_heads
        self.attention_head_size = hidden_size // num_attention_heads

        # Q, K, V Projektionen
        np.random.seed(42)
        self.W_q = np.random.randn(hidden_size, hidden_size) * 0.02
        self.W_k = np.random.randn(hidden_size, hidden_size) * 0.02
        self.W_v = np.random.randn(hidden_size, hidden_size) * 0.02
        self.W_o = np.random.randn(hidden_size, hidden_size) * 0.02

    def forward(self, hidden_states: np.ndarray, attention_mask: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Self-Attention forward pass

        Args:
            hidden_states: [batch, seq, hidden]
            attention_mask: [batch, seq]

        Returns:
            output: [batch, seq, hidden]
        """
        batch_size, seq_length, hidden_size = hidden_states.shape

        # Linear projections
        Q = np.dot(hidden_states, self.W_q)  # [batch, seq, hidden]
        K = np.dot(hidden_states, self.W_k)
        V = np.dot(hidden_states, self.W_v)

        # Reshape für Multi-Head Attention
        Q = self.transpose_for_scores(Q)  # [batch, heads, seq, head_size]
        K = self.transpose_for_scores(K)
        V = self.transpose_for_scores(V)

        # Attention scores
        attention_scores = np.matmul(Q, K.transpose(0, 1, 3, 2))  # [batch, heads, seq, seq]
        attention_scores = attention_scores / np.sqrt(self.attention_head_size)

        # Apply attention mask
        if attention_mask is not None:
            # Erweitere mask für multi-head
            attention_mask = np.expand_dims(attention_mask, axis=(1, 2))  # [batch, 1, 1, seq]
            attention_scores = attention_scores + (1.0 - attention_mask) * -10000.0

        # Softmax
        attention_probs = self.softmax(attention_scores)

        # Apply attention to values
        context = np.matmul(attention_probs, V)  # [batch, heads, seq, head_size]

        # Reshape zurück
        context = context.transpose(0, 2, 1, 3)  # [batch, seq, heads, head_size]
        context = context.reshape(batch_size, seq_length, hidden_size)

        # Output projection
        output = np.dot(context, self.W_o)

        return output

    def transpose_for_scores(self, x: np.ndarray) -> np.ndarray:
        """Reshape für Multi-Head Attention"""
        batch_size, seq_length, hidden_size = x.shape
        x = x.reshape(batch_size, seq_length, self.num_attention_heads, self.attention_head_size)
        return x.transpose(0, 2, 1, 3)  # [batch, heads, seq, head_size]

    def softmax(self, x: np.ndarray) -> np.ndarray:
        """Numerically stable softmax"""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


class MinimalBertLayer:
    """Einzelne BERT Layer (Attention + FFN)"""

    def __init__(self, hidden_size: int = 128, num_attention_heads: int = 4,
                 intermediate_size: int = 512):
        self.attention = MinimalBertSelfAttention(hidden_size, num_attention_heads)

        # Feed-Forward Network
        np.random.seed(42)
        self.W_1 = np.random.randn(hidden_size, intermediate_size) * 0.02
        self.b_1 = np.zeros(intermediate_size)
        self.W_2 = np.random.randn(intermediate_size, hidden_size) * 0.02
        self.b_2 = np.zeros(hidden_size)

        # LayerNorm
        self.ln1_gamma = np.ones(hidden_size)
        self.ln1_beta = np.zeros(hidden_size)
        self.ln2_gamma = np.ones(hidden_size)
        self.ln2_beta = np.zeros(hidden_size)

    def forward(self, hidden_states: np.ndarray, attention_mask: Optional[np.ndarray] = None) -> np.ndarray:
        """Forward pass durch BERT Layer"""

        # Self-Attention
        attention_output = self.attention.forward(hidden_states, attention_mask)

        # Add & Norm
        hidden_states = self.layer_norm(hidden_states + attention_output,
                                       self.ln1_gamma, self.ln1_beta)

        # Feed-Forward
        ff_output = np.dot(hidden_states, self.W_1) + self.b_1
        ff_output = self.gelu(ff_output)
        ff_output = np.dot(ff_output, self.W_2) + self.b_2

        # Add & Norm
        output = self.layer_norm(hidden_states + ff_output,
                                self.ln2_gamma, self.ln2_beta)

        return output

    def gelu(self, x: np.ndarray) -> np.ndarray:
        """GELU Activation"""
        return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))

    def layer_norm(self, x: np.ndarray, gamma: np.ndarray, beta: np.ndarray,
                   epsilon: float = 1e-12) -> np.ndarray:
        """Layer Normalization"""
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return gamma * (x - mean) / (std + epsilon) + beta


class MinimalBertForSentiment:
    """
    Minimal BERT Model für deutsche Sentiment-Analyse
    Nur mit NumPy - keine externen ML-Dependencies
    """

    def __init__(self, vocab_size: int = 500, hidden_size: int = 128,
                 num_hidden_layers: int = 2, num_attention_heads: int = 4,
                 intermediate_size: int = 512, num_labels: int = 3):
        """
        Initialisiert Mini-BERT Model

        Args:
            vocab_size: Größe des Vokabulars
            hidden_size: Größe der Hidden States
            num_hidden_layers: Anzahl BERT Layers
            num_attention_heads: Anzahl Attention Heads
            intermediate_size: Größe des FFN
            num_labels: Anzahl Sentiment-Klassen (3: neg, neutral, pos)
        """
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_labels = num_labels

        # Embeddings
        self.embeddings = MinimalBertEmbedding(vocab_size, hidden_size)

        # BERT Layers
        self.layers = [
            MinimalBertLayer(hidden_size, num_attention_heads, intermediate_size)
            for _ in range(num_hidden_layers)
        ]

        # Classifier Head
        np.random.seed(42)
        self.classifier_W = np.random.randn(hidden_size, num_labels) * 0.02
        self.classifier_b = np.zeros(num_labels)

        # Trainiert auf deutschem Sentiment-Korpus (simuliert durch Initialisierung)
        self._initialize_german_sentiment_weights()

    def _initialize_german_sentiment_weights(self):
        """
        Simuliert vortrainierte Gewichte für deutsche Sentiment-Analyse
        In echtem Szenario würden diese von einem trainierten Modell geladen
        """
        # Hier könnten vortrainierte Gewichte geladen werden
        # Für Demo: Angepasste Initialisierung
        pass

    def forward(self, input_ids: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        """
        Forward pass durch das Model

        Args:
            input_ids: [batch_size, seq_length]
            attention_mask: [batch_size, seq_length]

        Returns:
            logits: [batch_size, num_labels]
        """
        # Embeddings
        hidden_states = self.embeddings.forward(input_ids)

        # Durch alle BERT Layers
        for layer in self.layers:
            hidden_states = layer.forward(hidden_states, attention_mask)

        # Pool: Verwende [CLS] token (erste Position)
        pooled_output = hidden_states[:, 0, :]  # [batch_size, hidden_size]

        # Classification
        logits = np.dot(pooled_output, self.classifier_W) + self.classifier_b

        return logits

    def predict(self, input_ids: np.ndarray, attention_mask: np.ndarray) -> Dict:
        """
        Macht Sentiment-Prediction

        Args:
            input_ids: [batch_size, seq_length]
            attention_mask: [batch_size, seq_length]

        Returns:
            Dictionary mit Labels und Scores
        """
        logits = self.forward(input_ids, attention_mask)

        # Softmax für Wahrscheinlichkeiten
        probs = self.softmax(logits)

        # Predicted labels
        predicted_labels = np.argmax(probs, axis=-1)

        # Label mapping: 0=negative, 1=neutral, 2=positive
        label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}

        results = []
        for i in range(len(predicted_labels)):
            label_id = predicted_labels[i]
            results.append({
                'label': label_map[label_id],
                'label_id': int(label_id),
                'score': float(probs[i, label_id]),
                'all_scores': {
                    'negative': float(probs[i, 0]),
                    'neutral': float(probs[i, 1]),
                    'positive': float(probs[i, 2])
                }
            })

        return results

    def softmax(self, x: np.ndarray) -> np.ndarray:
        """Numerically stable softmax"""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def save(self, path: str):
        """Speichert Model-Gewichte"""
        model_dict = {
            'vocab_size': self.vocab_size,
            'hidden_size': self.hidden_size,
            'num_labels': self.num_labels,
            'embeddings': {
                'token': self.embeddings.token_embeddings,
                'position': self.embeddings.position_embeddings,
                'token_type': self.embeddings.token_type_embeddings,
                'gamma': self.embeddings.gamma,
                'beta': self.embeddings.beta
            },
            'classifier': {
                'W': self.classifier_W,
                'b': self.classifier_b
            }
            # Weitere Layer-Gewichte könnten hier gespeichert werden
        }

        with open(path, 'wb') as f:
            pickle.dump(model_dict, f)

    @classmethod
    def load(cls, path: str):
        """Lädt Model-Gewichte"""
        with open(path, 'rb') as f:
            model_dict = pickle.load(f)

        model = cls(
            vocab_size=model_dict['vocab_size'],
            hidden_size=model_dict['hidden_size'],
            num_labels=model_dict['num_labels']
        )

        # Lade Gewichte
        model.embeddings.token_embeddings = model_dict['embeddings']['token']
        model.embeddings.position_embeddings = model_dict['embeddings']['position']
        model.embeddings.token_type_embeddings = model_dict['embeddings']['token_type']
        model.embeddings.gamma = model_dict['embeddings']['gamma']
        model.embeddings.beta = model_dict['embeddings']['beta']
        model.classifier_W = model_dict['classifier']['W']
        model.classifier_b = model_dict['classifier']['b']

        return model


if __name__ == "__main__":
    # Test
    print("Initialisiere Minimal BERT Model...")
    model = MinimalBertForSentiment(
        vocab_size=500,
        hidden_size=128,
        num_hidden_layers=2,
        num_attention_heads=4,
        num_labels=3
    )

    # Test Input
    batch_size = 2
    seq_length = 16

    input_ids = np.random.randint(0, 500, size=(batch_size, seq_length))
    attention_mask = np.ones((batch_size, seq_length))

    # Forward pass
    print("\nForward pass...")
    results = model.predict(input_ids, attention_mask)

    for i, result in enumerate(results):
        print(f"\nSample {i+1}:")
        print(f"  Label: {result['label']}")
        print(f"  Confidence: {result['score']:.3f}")
        print(f"  All scores: {result['all_scores']}")

    # Save/Load Test
    print("\nSave model...")
    model.save('/tmp/test_model.pkl')
    print("Load model...")
    loaded_model = MinimalBertForSentiment.load('/tmp/test_model.pkl')
    print("Model loaded successfully!")
