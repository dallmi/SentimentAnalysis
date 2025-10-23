# Manual BERT Model Download Guide

## Problem
If `setup_offline_model.py` fails due to SSL certificate errors in corporate environments, use this manual download method.

## Solution: Download Model on Personal Computer, Transfer to Corporate Laptop

---

## Step 1: Download on Personal Computer (with internet)

### Option A: Using Python Script

On your **personal computer** (not corporate laptop):

```bash
# Clone or download this repository
git clone https://github.com/dallmi/SentimentAnalysis.git
cd SentimentAnalysis

# Install dependencies
pip install transformers torch

# Run download script (on personal computer, this should work)
python setup_offline_model.py
```

This creates: `models/bert-base-multilingual-uncased-sentiment/`

### Option B: Using Git LFS

On your **personal computer**:

```bash
# Install git-lfs if not already installed
# macOS: brew install git-lfs
# Windows: Download from https://git-lfs.github.com/
# Linux: sudo apt-get install git-lfs

# Initialize git-lfs
git lfs install

# Clone the model directly from HuggingFace
git clone https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment

# This creates folder: bert-base-multilingual-uncased-sentiment/
```

### Option C: Manual Download via Browser

1. Go to: https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment/tree/main

2. Download these files (click "Download" on each):
   - `config.json` (small)
   - `pytorch_model.bin` (~600MB - this is the big one!)
   - `tokenizer_config.json` (small)
   - `vocab.txt` (small)
   - `tokenizer.json` (small)
   - `special_tokens_map.json` (small)

3. Create folder structure on your personal computer:
   ```
   bert-base-multilingual-uncased-sentiment/
   ├── config.json
   ├── pytorch_model.bin
   ├── tokenizer_config.json
   ├── vocab.txt
   ├── tokenizer.json
   └── special_tokens_map.json
   ```

---

## Step 2: Transfer to Corporate Laptop

### Option A: USB Stick (Recommended)

1. **On personal computer:**
   ```bash
   # Copy the model folder to USB
   cp -r bert-base-multilingual-uncased-sentiment /Volumes/YOUR_USB_NAME/
   # or on Windows:
   # xcopy bert-base-multilingual-uncased-sentiment E:\bert-base-multilingual-uncased-sentiment /E /I
   ```

2. **On corporate laptop:**
   ```bash
   # Navigate to SentimentAnalysis repository
   cd /path/to/SentimentAnalysis

   # Create models directory if it doesn't exist
   mkdir -p models

   # Copy from USB to models folder
   cp -r /Volumes/YOUR_USB_NAME/bert-base-multilingual-uncased-sentiment models/
   # or on Windows:
   # xcopy E:\bert-base-multilingual-uncased-sentiment models\bert-base-multilingual-uncased-sentiment /E /I
   ```

### Option B: ZIP and Email/File Share

1. **On personal computer:**
   ```bash
   # Create ZIP file
   zip -r bert-model.zip bert-base-multilingual-uncased-sentiment/
   ```

2. **Transfer ZIP:**
   - Email to yourself (if file size < corporate limit, usually 25-50 MB)
   - Upload to corporate file share (SharePoint, network drive)
   - Upload to cloud storage if allowed (OneDrive, Dropbox)

3. **On corporate laptop:**
   ```bash
   # Extract ZIP
   unzip bert-model.zip

   # Move to correct location
   mv bert-base-multilingual-uncased-sentiment /path/to/SentimentAnalysis/models/
   ```

### Option C: Cloud Storage (if allowed)

1. **On personal computer:**
   - Upload `bert-base-multilingual-uncased-sentiment/` folder to OneDrive/Dropbox/Google Drive

2. **On corporate laptop:**
   - Download from cloud storage
   - Move to `SentimentAnalysis/models/`

---

## Step 3: Verify Installation

On your **corporate laptop**:

```bash
# Navigate to repository
cd /path/to/SentimentAnalysis

# Check if model files exist
ls -lh models/bert-base-multilingual-uncased-sentiment/

# Should show:
# config.json
# pytorch_model.bin (~600MB)
# tokenizer_config.json
# vocab.txt
# tokenizer.json
# special_tokens_map.json
```

Expected total size: **~600-650 MB**

---

## Step 4: Test the Model

```bash
# Test if model works offline
python -c "
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

model_path = Path('models/bert-base-multilingual-uncased-sentiment')

print('Loading tokenizer...')
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
print('✓ Tokenizer loaded')

print('Loading model...')
model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
print('✓ Model loaded')

print('Testing inference...')
text = 'This is a great article!'
inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
outputs = model(**inputs)
print('✓ Model works!')
print(f'Output shape: {outputs.logits.shape}')
"
```

If you see:
```
✓ Tokenizer loaded
✓ Model loaded
✓ Model works!
Output shape: torch.Size([1, 5])
```

Then **SUCCESS!** The model is ready to use offline.

---

## Step 5: Run Analysis

Now you can run the sentiment analysis:

```bash
python main.py --input data/input/your_articles.xlsx
```

The system will use the offline model automatically.

---

## Troubleshooting

### "No module named 'transformers'"
```bash
pip install transformers torch
```

### "Model not found"
Check the path:
```bash
# Should be exactly:
SentimentAnalysis/
└── models/
    └── bert-base-multilingual-uncased-sentiment/
        ├── config.json
        ├── pytorch_model.bin
        └── ... (other files)
```

### "Permission denied"
On corporate laptop:
```bash
# Check permissions
ls -l models/bert-base-multilingual-uncased-sentiment/

# Fix if needed
chmod -R 755 models/
```

### Model files corrupted during transfer
- Verify file sizes match:
  - `pytorch_model.bin` should be ~600MB
  - If smaller, re-download on personal computer

---

## Summary

**Easiest method:** USB stick transfer
1. Download on personal computer (Option A, B, or C)
2. Copy to USB
3. Transfer to corporate laptop
4. Test with verification script

**Total time:** ~15-30 minutes (including download time)

---

## Next Steps

Once model is installed:
1. ✅ Model is in `models/bert-base-multilingual-uncased-sentiment/`
2. ✅ Verification script passed
3. ✅ Run analysis: `python main.py --input your_file.xlsx`

The system is now fully offline and ready for corporate use!
