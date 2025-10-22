# Categorization Modes: Supervised vs. Unsupervised

## 🎯 Two Approaches to Understanding Your Articles

The system now supports **two different ways** to categorize your articles:

### 1️⃣ **Supervised Mode** (Predefined Categories) - DEFAULT

Uses predefined content themes that you specify in advance.

**When to use:**
- ✅ You know what topics to expect (AI, Employee Stories, Events, etc.)
- ✅ You want consistent categories across time periods
- ✅ You want to track specific themes you care about
- ✅ You want to compare against your content strategy

**How it works:**
- Uses 10 predefined categories (configurable in `config/settings.py`)
- Matches article text against keyword lists
- Categories: AI & Innovation, Employee Stories, Culture & Values, etc.

**Command:**
```bash
python main_with_llm.py --input data/input/articles.xlsx
```

**Example Output:**
```
Content Theme         | Articles | Avg Sentiment
---------------------|----------|---------------
Employee Stories     | 25       | +0.88
Events & Networking  | 20       | +0.75
AI & Innovation      | 30       | +0.45
```

---

### 2️⃣ **Unsupervised Mode** (Automatic Topic Discovery) - NEW! 🆕

Automatically discovers what your articles are about WITHOUT predefined categories.

**When to use:**
- ✅ You don't know what topics to expect
- ✅ You want to discover emerging themes
- ✅ Your content is diverse and unpredictable
- ✅ You want data-driven insights rather than assumptions
- ✅ You want to see what employees ACTUALLY write about

**How it works:**
- Uses TF-IDF (Term Frequency-Inverse Document Frequency)
- Applies K-Means clustering algorithm
- Automatically names topics based on top keywords
- Discovers natural groupings in your data

**Command:**
```bash
python main_with_llm.py --input data/input/articles.xlsx --discover-topics
```

**Example Output:**
```
Discovered Topics           | Articles | Top Keywords
---------------------------|----------|---------------------------
Remote & Hybrid            | 18       | remote, homeoffice, flexibility
ChatGPT & Automation       | 22       | chatgpt, automation, workflow
Team Building & Culture    | 15       | teambuilding, celebration, culture
Leadership Changes         | 8        | leadership, restructuring, change
```

---

## 📊 Comparison: Supervised vs. Unsupervised

| Aspect | Supervised | Unsupervised |
|--------|-----------|--------------|
| **Setup** | Define categories in advance | No setup needed |
| **Categories** | Consistent, predictable | Data-driven, may vary |
| **Best for** | Known topics, tracking trends | Discovery, exploration |
| **Flexibility** | Must update keywords manually | Adapts automatically |
| **Interpretability** | Easy to understand | Requires interpretation |
| **Use case** | "Track performance of AI articles" | "What are people writing about?" |

---

## 🚀 Usage Examples

### Example 1: Standard Analysis with Predefined Categories

```bash
# Use default 10 predefined categories
python main_with_llm.py --input data/input/q4_articles.xlsx
```

**Best for:** Regular quarterly reports, tracking known content themes

---

### Example 2: Discover What Topics Actually Appear

```bash
# Let the system discover 10 topics automatically
python main_with_llm.py --input data/input/q4_articles.xlsx --discover-topics
```

**Best for:** First-time analysis, understanding your content landscape

---

### Example 3: Discover More Topics

```bash
# Discover 15 topics (more granular)
python main_with_llm.py --input data/input/q4_articles.xlsx --discover-topics --num-topics 15
```

**Best for:** Large datasets, finding niche topics

---

### Example 4: Discover Fewer Topics

```bash
# Discover only 5 broad topics
python main_with_llm.py --input data/input/q4_articles.xlsx --discover-topics --num-topics 5
```

**Best for:** High-level overview, executive summaries

---

## 🎯 Which Mode Should You Use?

### Use **Supervised Mode** when:

**Scenario 1: Quarterly Content Performance**
> "I want to see if our AI & Innovation articles improved compared to last quarter"

→ Use predefined categories to ensure consistency across quarters

**Scenario 2: Content Strategy Tracking**
> "We decided to publish more Employee Stories. Is it working?"

→ Use predefined "Employee Stories" category to track specific initiative

**Scenario 3: Department-Specific Analysis**
> "HR wants to know if their wellness articles are well-received"

→ Use predefined "Wellness & Benefits" category

---

### Use **Unsupervised Mode** when:

**Scenario 1: First-Time Analysis**
> "I have 500 articles from the past year. What are they about?"

→ Let the system discover natural topic groupings

**Scenario 2: Finding Emerging Themes**
> "Are there new topics employees are interested in that we're not tracking?"

→ Discover topics automatically to find surprises

**Scenario 3: Validating Assumptions**
> "We think we publish a lot about AI. Is that actually true?"

→ See what topics emerge naturally from the data

**Scenario 4: Diverse Content**
> "Our intranet has everything from recipes to software updates"

→ Unsupervised mode handles unpredictable content better

---

## 🔬 Technical Details

### Supervised Categorization

**Algorithm:** Keyword Matching with TF-IDF weighting

**Process:**
1. Load predefined categories from `config/settings.py`
2. For each article, count keyword matches
3. Assign article to category with highest score
4. Extract top keywords from article text

**Strengths:**
- Fast and predictable
- Easy to explain to stakeholders
- Consistent over time
- Can customize keywords for your domain

**Weaknesses:**
- Misses topics you didn't anticipate
- Requires manual keyword maintenance
- May force articles into wrong categories

---

### Unsupervised Topic Discovery

**Algorithm:** TF-IDF + K-Means Clustering

**Process:**
1. Convert all articles to TF-IDF vectors
2. Apply K-Means clustering
3. For each cluster, extract top keywords
4. Generate topic name from keywords
5. Assign sentiment statistics per topic

**Strengths:**
- Discovers unexpected topics
- No manual keyword maintenance
- Data-driven, objective
- Adapts to new content automatically

**Weaknesses:**
- Topic names may need interpretation
- Categories not consistent across runs
- Less control over granularity
- May create odd groupings with small datasets

---

## 💡 Best Practice: Use Both!

**Recommended Workflow:**

### Step 1: Discovery (Unsupervised)
```bash
# First, discover what topics exist
python main_with_llm.py --input articles.xlsx --discover-topics
```

**Review the discovered topics:**
- "Remote & Hybrid" - 18 articles, +0.72 sentiment
- "ChatGPT & Automation" - 22 articles, +0.45 sentiment
- "Leadership Changes" - 8 articles, -0.15 sentiment

### Step 2: Customize Categories (Supervised)

Based on discoveries, update `config/settings.py`:

```python
CATEGORY_KEYWORDS = {
    # Add discovered topic as permanent category
    'Remote Work & Flexibility': [
        'remote', 'homeoffice', 'hybrid', 'flexible', 'work from home',
        # ... add more keywords
    ],

    # Rename existing category based on what you learned
    'AI & Automation': [  # Was: 'AI & Innovation'
        'ai', 'chatgpt', 'automation', 'gpt', 'copilot',
        # ... discovered "automation" is key term
    ],
}
```

### Step 3: Track Over Time (Supervised)
```bash
# Now use customized categories for quarterly tracking
python main_with_llm.py --input q1_articles.xlsx
python main_with_llm.py --input q2_articles.xlsx
python main_with_llm.py --input q3_articles.xlsx
```

**Compare trends:**
- Remote Work articles: Q1: 12 (+0.65) → Q2: 18 (+0.72) → Q3: 25 (+0.78) ✅ Growing & positive!

---

## 📈 Report Differences

### Supervised Mode Excel Report

**Sheet "Kategorien":**
| Content Theme | Avg_Sentiment | Articles |
|--------------|---------------|----------|
| Employee Stories | +0.88 | 25 |
| AI & Innovation | +0.45 | 30 |

→ **Consistent category names**

---

### Unsupervised Mode Excel Report

**Sheet "Kategorien":**
| Discovered Topic | Avg_Sentiment | Articles |
|-----------------|---------------|----------|
| Interview & Career | +0.92 | 18 |
| Chatgpt & Automation | +0.48 | 22 |
| Remote & Flexibility | +0.75 | 15 |

→ **Data-driven topic names from keywords**

---

## ⚙️ Advanced Options

### Adjust Number of Topics

```bash
# Too many small topics? Use fewer:
python main_with_llm.py --input articles.xlsx --discover-topics --num-topics 5

# Want more granular topics? Use more:
python main_with_llm.py --input articles.xlsx --discover-topics --num-topics 20
```

**Guidelines:**
- **5-7 topics:** High-level overview, executive summary
- **10-12 topics:** Standard analysis (default)
- **15-20 topics:** Detailed analysis for large datasets
- **20+ topics:** Risk of very small, meaningless clusters

---

## 🎓 Example Insights from Each Mode

### Supervised Mode Insights

> "Employee Stories get +0.88 sentiment → Create more!"
> "Organizational Change gets -0.15 sentiment → Improve communication!"

**Actionable:** You decided to track these categories, so you can act on them directly.

---

### Unsupervised Mode Insights

> "Discovered topic 'ChatGPT & Productivity' (22 articles, +0.55 sentiment)"
> "This wasn't in our predefined categories - employees are very interested!"

**Discovering:** You didn't know this was a theme, but data shows it's important.

> "Topic 'Office Redesign & Furniture' appeared (8 articles, -0.22 sentiment)"
> "Ah, that explains the negative feedback last month!"

**Understanding:** Explains sentiment patterns you couldn't explain before.

---

## 🆘 Troubleshooting

### "Topics look weird / not meaningful"

**Possible causes:**
- Too few articles (need at least 20-30 for good results)
- Too many topics requested (try fewer)
- Articles too short or similar

**Solutions:**
```bash
# Try fewer topics
python main_with_llm.py --input articles.xlsx --discover-topics --num-topics 5

# Or use supervised mode for small datasets
python main_with_llm.py --input articles.xlsx
```

---

### "Want both supervised AND discovered topics in same report"

**Current limitation:** You can only use one mode per run.

**Workaround:** Run twice and compare:
```bash
# Run 1: Supervised
python main_with_llm.py --input articles.xlsx
# → data/output/llm_analysis_20251022_120000.xlsx

# Run 2: Unsupervised
python main_with_llm.py --input articles.xlsx --discover-topics
# → data/output/llm_analysis_20251022_120500.xlsx

# Open both Excel files and compare!
```

---

## 📖 Summary

**Quick Decision Matrix:**

| Your Situation | Recommended Mode |
|----------------|------------------|
| "First time using this system" | `--discover-topics` |
| "I know exactly what I'm looking for" | Default (supervised) |
| "Want to track AI articles over time" | Default (supervised) |
| "Not sure what content we have" | `--discover-topics` |
| "Want to find surprising insights" | `--discover-topics` |
| "Need consistent reports quarterly" | Default (supervised) |
| "Have <30 articles" | Default (supervised) |
| "Have >100 diverse articles" | `--discover-topics` |

**Best of both worlds:** Start with `--discover-topics` to explore, then customize supervised categories based on discoveries! 🎯
