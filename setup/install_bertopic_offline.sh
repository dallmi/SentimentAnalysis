#!/bin/bash
# BERTopic Offline Installation Script

echo "Installing BERTopic and dependencies..."

cd "$(dirname "$0")/offline_packages/bertopic"

pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan plotly kaleido

if [ $? -eq 0 ]; then
    echo "✓ Installation successful!"
    echo ""
    echo "Testing installation..."
    python -c "import bertopic; import sentence_transformers; import umap; import hdbscan; print('✓ All packages work!')"
else
    echo "❌ Installation failed. Try installing dependencies manually:"
    echo "   pip install --no-index --find-links . *"
fi
