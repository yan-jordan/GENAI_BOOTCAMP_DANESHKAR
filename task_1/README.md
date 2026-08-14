# 📝 TextProcessor: Word Frequency Analyzer

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-stdlib%20only-brightgreen.svg)

## 📖 Overview

**TextProcessor** ([`class_template.py`](./class_template.py)) is a small,
dependency-free Python class that analyzes a text file: it strips URLs,
emails, and punctuation, tokenizes the remaining text, filters out a
built-in list of English stop words, counts how often every remaining word
appears, and writes the result out as JSON.

The script's own example run reads [`input2.txt`](./input2.txt) and writes
[`result.json`](./result.json) — both already present in this folder, so
you can compare `result.json` against `input2.txt` to see exactly what the
pipeline produces.

---

## ✨ Key Features

- **🧹 URL & Email Stripping:** Regex-based removal of URLs and email addresses before anything else runs.
- **✂️ Punctuation Stripping:** Removes every standard punctuation character so `"hello!"` and `"hello"` aren't counted as different words.
- **🛑 Stop Word Filtering:** Filters against a small, hardcoded `set` of common English stop words (`and`, `the`, `is`, `for`, ...).
- **📊 Frequency Counting:** Tallies occurrences of every remaining word.
- **💾 JSON Export:** Writes the frequency dictionary to a pretty-printed (`indent=4`) JSON file.

---

## 🛠️ Prerequisites

Built entirely on Python's **standard library** — nothing to `pip install`.

- Python 3.6+
- `re`, `json`, `string` (all standard library)

---

## 🚀 Usage

The bottom of `class_template.py` already wires up an example run:

```python
processor = TextProcessor("input2.txt", "word_frequencies.json")
processor.process()
```

So simply:

```bash
python class_template.py
```

This reads `input2.txt` (already in this folder) and writes the frequency
dictionary to `result.json`.

To analyze a different file, either edit the two arguments at the bottom of
the script, or import the class yourself:

```python
from class_template import TextProcessor

processor = TextProcessor(file_path="my_input.txt", output_json="my_output.json")
processor.process()
```

⚠️ See **Known Issues** below — the `output_json` argument is currently
cosmetic; the result always lands in a file literally named `result.json`.

### Example

Given input text like:

```text
Hello world! Welcome to the world of Python.
If you have questions, email us at contact@example.com or visit https://python.org.
```

`class_template.py` produces a JSON file shaped like:

```json
{
    "Hello": 1,
    "world": 2,
    "Welcome": 1,
    "Python": 1,
    "questions": 1,
    "email": 1,
    "us": 1,
    "visit": 1
}
```

(URLs, the email address, and stop words like `to`, `the`, `of`, `you`,
`have`, `at`, `or` are all removed before counting.)

---

## 🏗️ Pipeline

`TextProcessor.process()` runs a 6-step pipeline:

1. **`read_file()`** — reads the raw text from `self.file_path`.
2. **`clean_text()`** — regexes out URLs and emails, then strips punctuation.
3. **Tokenization** — `.split()` on the cleaned string.
4. **`remove_stopwords()`** — filters tokens against `self.stop_words`.
5. **`count_word_frequencies()`** — counts occurrences of each remaining word.
6. **`save_to_json()`** — writes the frequency dict to `result.json`.

---

## ⚙️ Customization

### Adding stop words

Extend the `self.stop_words` set in `__init__`:

```python
self.stop_words = set([
    "and", "in", "to", "from", "that", "this", "the",  # ...
    "your_custom_word1", "your_custom_word2"
])
```

### Case sensitivity

`clean_text()` does **not** lowercase text, so counting is currently
case-sensitive (`"Code"` and `"code"` are counted separately). To make it
case-insensitive, lowercase the text before returning it from
`clean_text()`.

---

## 🐞 Known Issues

- **`output_json` is unused.** `TextProcessor.__init__` stores
  `self.output_json`, but `save_to_json()` ignores it and always writes to
  a hardcoded `"result.json"`. Passing a different filename to the
  constructor has no effect on where the output actually goes.
- **`count_word_frequencies()` is O(n²).** It compares every token against
  every other token in a nested loop rather than using a single pass (e.g.
  `collections.Counter`). The output is correct, but it will get slow on
  large input files.
