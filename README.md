# 🕷️ Wikipedia Crawler (Speer Assessment)

This Python script recursively crawls Wikipedia articles starting from a given valid Wikipedia link. It collects and stores the **first 10 unique Wikipedia links** found on each page for up to **N depth levels**. This was developed as part of an assessment for a QA role at Speer Technologies.

---

## 🚀 Features

- Accepts a valid Wikipedia article URL
- Accepts a depth level (1 to 3)
- Recursively collects unique links (no duplicates, no revisits)
- Optionally outputs to JSON or CSV
- Built-in validation and error handling

---

## 📦 Requirements

The script uses two external libraries that are **not built-in**. You must install them before running:

```bash
pip install requests beautifulsoup4
````

## 📁 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/faisalqob/wikipedia-crawler.git
   cd wikipedia-crawler
   ```

2. Install dependencies:

   ```bash
   pip install requests
   pip install bs4
   ```
---

## 🧠 Usage

Run the script using:

```bash
python test.py <wiki-url> <depth> --out <csv|json>
```

**Arguments**:

* `<wiki-url>`: A valid Wikipedia article URL
* `<depth>`: An integer between 1 and 3
* `--out`: (Optional) Output format (`csv` or `json`). Default is `json`

---

## 📌 Examples

```bash
# Crawl Canada Wikipedia article to depth 2, save output as JSON
python test.py "https://en.wikipedia.org/wiki/Canada" 2 --out json

# Crawl Python (programming language) article to depth 3, save as CSV
python test.py "https://en.wikipedia.org/wiki/Python_(programming_language)" 3 --out csv

# Invalid URL (will raise error)
python test.py "https://google.com" 1
```

---

## 📤 Output

* All crawled links are stored in either:

  * `wiki_links.json`
  * `wiki_links.csv`

Each entry includes:

* Source page
* Target linked page

---

## ⚠️ Notes

* The script will not revisit already visited links.
* Invalid Wikipedia links will be rejected with an error.
* Depth must be between 1 and 3.

---

## 📄 License
© 2025 Faisal Yakubu

```
