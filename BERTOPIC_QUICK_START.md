# BERTopic Quick Start Guide

## 🎯 What is BERTopic?

BERTopic is an advanced topic modeling library that:
- Uses BERT embeddings to understand document meaning
- Automatically finds optimal number of topics
- Creates better topic labels than traditional methods
- Supports visualization of topics

## 📦 Offline Setup (For Corporate Environment)

### On Your Personal Computer (with Internet):

```bash
# 1. Download all packages and models
python setup_bertopic_offline.py

# This downloads (~900MB):
# - bertopic package
# - sentence-transformers
# - umap-learn
# - hdbscan
# - Pre-trained models
```

### Transfer to Corporate Environment:

Transfer the entire `SentimentAnalysis` folder via:
- Approved transfer method

### In Corporate Environment:

```bash
# Option A: Use installation script (Mac/Linux)
bash install_bertopic_offline.sh

# Option B: Manual installation (Windows)
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

## 🚀 Basic Usage

### Example 1: Simple Topic Modeling

```python
from bertopic import BERTopic

# Your article texts
texts = [
    "New AI tools for employees to improve productivity",
    "Employee wellness program launches next month",
    "Machine learning workshop for beginners",
    "Health benefits update for 2024"
]

# Create BERTopic model
topic_model = BERTopic()

# Find topics
topics, probabilities = topic_model.fit_transform(texts)

# Get topic info
print(topic_model.get_topic_info())
```

**Output:**
```
Topic  Count  Name
-1     1      -1_outliers
0      2      0_ai_tools_machine
1      2      1_wellness_health_benefits
```

### Example 2: With Offline Model

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Load offline model
sentence_model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')

# Create BERTopic with offline model
topic_model = BERTopic(embedding_model=sentence_model)

# Analyze
topics, probs = topic_model.fit_transform(article_texts)
```

### Example 3: Get Topics for Each Document

```python
# Get topic for each document
for i, (text, topic) in enumerate(zip(texts, topics)):
    topic_name = topic_model.get_topic(topic)
    print(f"Document {i}: Topic {topic}")
    print(f"  Keywords: {topic_name[:5]}")  # Top 5 keywords
    print(f"  Text: {text[:50]}...")
```

### Example 4: Visualize Topics

```python
# Create interactive topic visualization
fig = topic_model.visualize_topics()
fig.write_html("topic_visualization.html")

# Create topic hierarchy
fig = topic_model.visualize_hierarchy()
fig.write_html("topic_hierarchy.html")
```

## 🎨 Integration with Sentiment Analysis

### Combine BERTopic with Your Sentiment Data

```python
import pandas as pd
from bertopic import BERTopic

# Your data
articles_df = pd.DataFrame({
    'text': ['Article 1...', 'Article 2...'],
    'sentiment': [0.65, -0.23],
    'title': ['AI Tools', 'Policy Update']
})

# Find topics
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(articles_df['text'].tolist())

# Add to dataframe
articles_df['topic'] = topics
articles_df['topic_name'] = [topic_model.get_topic(t) for t in topics]

# Analyze sentiment by topic
sentiment_by_topic = articles_df.groupby('topic')['sentiment'].mean()
print(sentiment_by_topic)
```

**Output:**
```
topic
0    0.65  # AI-related topics (positive)
1   -0.23  # Policy topics (negative)
```

## 🆚 BERTopic vs. Current System

| Feature | Current System | BERTopic |
|---------|---------------|----------|
| Clustering | KMeans | HDBSCAN (better) |
| Topic Count | Manual tuning | Automatic |
| Topic Labels | Keyword extraction | Better labels |
| Visualization | None | Interactive plots |
| Outlier Handling | None | Yes (-1 topic) |
| Dependencies | Fewer | More |

## ⚙️ Advanced Configuration

### Control Number of Topics

```python
from bertopic import BERTopic

# Set minimum topic size
topic_model = BERTopic(min_topic_size=2)

# Or use manual number of topics
topic_model = BERTopic(nr_topics=5)
```

### Multilingual Support

```python
from sentence_transformers import SentenceTransformer

# Use multilingual model
multilingual_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

topic_model = BERTopic(
    embedding_model=multilingual_model,
    language='multilingual'
)
```

### Custom Topic Representation

```python
from bertopic.representation import MaximalMarginalRelevance

# Better topic labels
representation_model = MaximalMarginalRelevance(diversity=0.3)

topic_model = BERTopic(
    representation_model=representation_model
)
```

## 🔍 Troubleshooting

### Import Error

```
ImportError: No module named 'bertopic'
```

**Solution:** Install offline packages:
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic
```

### Model Download Error

```
Error downloading model from HuggingFace
```

**Solution:** Use offline model:
```python
model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')
```

### UMAP/HDBSCAN Errors

```
ImportError: No module named 'umap' or 'hdbscan'
```

**Solution:** Install dependencies:
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . umap-learn hdbscan
```

## 📊 Example: Full Analysis

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd

# Load data
df = pd.read_json('article_content.json')

# Prepare texts
texts = (df['title'] + '. ' + df['content']).tolist()

# Load offline model
sentence_model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')

# Create BERTopic model
topic_model = BERTopic(
    embedding_model=sentence_model,
    min_topic_size=2,
    nr_topics='auto'
)

# Find topics
topics, probs = topic_model.fit_transform(texts)

# Add to dataframe
df['topic'] = topics
df['topic_prob'] = probs

# Get topic names
for topic in set(topics):
    if topic != -1:  # Skip outliers
        keywords = topic_model.get_topic(topic)
        print(f"Topic {topic}: {keywords[:5]}")

# Analyze sentiment by topic
df['sentiment'] = df['comments'].apply(lambda x: calculate_sentiment(x))
topic_sentiment = df.groupby('topic')['sentiment'].agg(['mean', 'count'])
print(topic_sentiment)
```

## 🎓 Learn More

- **BERTopic Documentation**: https://maartengr.github.io/BERTopic/
- **Tutorial**: https://maartengr.github.io/BERTopic/getting_started/quickstart/quickstart.html
- **Examples**: https://github.com/MaartenGr/BERTopic/tree/master/notebooks

## 💡 When to Use BERTopic vs. Current System

**Use Current System When:**
- ✅ You want simple, fast analysis
- ✅ Fewer dependencies = better for corporate
- ✅ You have full control over clustering

**Use BERTopic When:**
- ✅ You want better topic discovery
- ✅ You don't know optimal number of topics
- ✅ You want visualizations
- ✅ You have complex/diverse content
