BERTopic Offline Installation Package for Windows
==================================================

This package contains all files needed to install BERTopic offline on Windows.

INSTALLATION:
-------------
1. Copy this entire folder to your Windows PC
2. Open Command Prompt (cmd.exe)
3. Navigate to the offline_packages folder
4. Run: install_bertopic_offline_windows.bat

OR manually:
   cd offline_packages\bertopic_windows
   pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan

MODELS:
-------
Pre-trained models are in: offline_packages/models/
- all-MiniLM-L6-v2 (English, fast)
- paraphrase-multilingual-MiniLM-L12-v2 (50+ languages incl. German)

USAGE:
------
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Load multilingual model
model = SentenceTransformer('offline_packages/models/paraphrase-multilingual-MiniLM-L12-v2')
topic_model = BERTopic(embedding_model=model)

# Analyze documents
docs = ["Your text here", "Another document"]
topics, probs = topic_model.fit_transform(docs)

REQUIREMENTS:
-------------
- Windows 7/10/11 (64-bit)
- Python 3.9 or newer
- pip installed

For more information, see BERTOPIC_OFFLINE_INSTALL.md
