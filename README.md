# 🕸️ Webpage Intent Matcher

This project crawls a website's **homepage (depth 0)** to collect all **first-level internal links**, then uses **semantic similarity and an LLM** to identify the most relevant webpage for a given user intent.

---

## Features

-  **Async Playwright-based crawler** — extracts all first-level (depth 0) internal links.  
-  **Excludes external URLs** and fragments (`#...`).  
-  **Semantic intent matching** using `SentenceTransformer (all-MiniLM-L6-v2)`.  
-  **LLM-powered reasoning layer** for the final intent-to-page match.  
-  Lightweight, accurate, and suitable for small-to-medium websites.  

---

## Workflow Overview

1. **Extract internal links (depth 0)** using Playwright.  
2. **Embed** the user's intent and all page URLs using `SentenceTransformer`.  
3. **Rank** pages by cosine similarity.  
4. **Send top-ranked candidates** to the LLM for final reasoning.  
5. **Output** only the most relevant URL as a plain string.

---

## Example

### Input

```python
base_url = "https://www.kecktm.edu.np/"
intent = "all department heads"
```

### Output

```
all department heads may be found at "https://www.kecktm.edu.np/faculty-and-staff/staff"
```

---

## Installation

```bash
# Install dependencies
pip install playwright beautifulsoup4 sentence-transformers torch langchain openai

# Install Playwright browser engine
playwright install chromium
```

---

## Parameters

| Parameter | Description | Default |
|------------|-------------|----------|
| `base_url` | Website homepage to start crawling | Required |
| `timeout` | Page load timeout (seconds) | `30` |
| `wait_for_load` | Wait time for JS rendering | `2` |
| `headless` | Run browser in headless mode | `True` |

---

## Notes

- Avoid crawling large or media-heavy websites. This script only fetches **depth 0** links for efficiency.  
- The LLM prompt is designed to ensure **minimal output format** — just the URL.  

---

## Example Output

```
[INFO] Starting single-page crawl for links: https://www.kecktm.edu.np/
[INFO] Found 64 total anchor tags.
[INFO] Extracted 28 internal links.

all department heads may be found at "https://www.kecktm.edu.np/faculty-and-staff/staff"
```

---