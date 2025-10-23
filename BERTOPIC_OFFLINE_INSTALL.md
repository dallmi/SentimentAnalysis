# BERTopic Offline Installation Guide

## Files in this package:

1. **offline_packages/bertopic/** - All Python packages (.whl files)
2. **offline_packages/models/** - Pre-trained sentence transformer models
3. **setup_bertopic_offline.py** - This setup script
4. **install_bertopic_offline.sh** - Installation script for corporate environment

## Installation Steps (Corporate Environment):

### Step 1: Transfer Files

Transfer this entire folder to your corporate environment:
- Via approved file transfer method

### Step 2: Install Packages

On your corporate machine (Windows):
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

On your corporate machine (Mac/Linux):
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan
```

Or use the installation script:
```bash
bash install_bertopic_offline.sh
```

### Step 3: Verify Installation

```python
# Test if packages are installed
python -c "import bertopic; import sentence_transformers; import umap; import hdbscan; print('✓ All packages installed!')"
```

### Step 4: Use Pre-trained Models

The models are already downloaded in `offline_packages/models/`.

To use them:
```python
from sentence_transformers import SentenceTransformer

# Load offline model
model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')
```

## Troubleshooting

### Missing Dependencies

If you get errors about missing dependencies, install them:
```bash
cd offline_packages/bertopic
pip install --no-index --find-links . *
```

### SSL Certificate Errors

If you get SSL errors when loading models, set:
```python
import os
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
```

### Model Loading Errors

If models don't load, you can download them manually in corporate environment:
```python
from sentence_transformers import SentenceTransformer

# This will download from HuggingFace (if allowed)
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('./offline_packages/models/all-MiniLM-L6-v2')
```

## Package Sizes

- bertopic: ~10MB
- sentence-transformers: ~100MB
- umap-learn: ~50MB
- hdbscan: ~30MB
- Pre-trained models: ~500MB
- Dependencies: ~200MB

**Total: ~900MB**

## Next Steps

After installation, you can use BERTopic in your sentiment analysis:

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Load offline model
sentence_model = SentenceTransformer('./offline_packages/models/all-MiniLM-L6-v2')

# Create BERTopic model
topic_model = BERTopic(embedding_model=sentence_model)

# Analyze your articles
topics, probs = topic_model.fit_transform(article_texts)

# Get topic info
topic_model.get_topic_info()
```

## Need Help?

Check the documentation:
- BERTopic: https://maartengr.github.io/BERTopic/
- Sentence Transformers: https://www.sbert.net/

