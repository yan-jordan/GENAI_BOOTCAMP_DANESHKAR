# 📝 TextProcessor: Advanced Word Frequency Analyzer

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## 📖 Overview

**TextProcessor** is a lightweight, dependency-free Python utility designed to analyze text documents. It processes raw text through a multi-stage pipeline that cleans unwanted elements, normalizes the text, filters out common filler words, and calculates the exact frequency of every unique word used in the document. Finally, the analyzed data is exported to a clean, structured JSON format.

Whether you are doing basic Natural Language Processing (NLP), parsing large documents, or analyzing text datasets, TextProcessor provides a solid and easily extensible foundation.

---

## ✨ Key Features

- **🧹 Automated Text Cleaning:** Uses robust Regular Expressions (Regex) to detect and instantly remove URLs and email addresses.
- **✂️ Punctuation Stripping:** Automatically clears all standard punctuation marks to prevent redundant word entries (e.g., counting "hello!" and "hello" as the same word).
- **🛑 Stop Word Filtering:** Comes with a built-in, customizable set of standard English stop words (like "and", "the", "is") so your frequency analysis focuses only on meaningful vocabulary.
- **📊 Frequency Mapping:** Counts the exact number of occurrences for every word in the document.
- **💾 JSON Export:** Outputs the final dictionary of word counts into a highly readable, indented JSON file for easy integration with other tools or web applications.

---

## 🛠️ Prerequisites

This project is built entirely using Python's **Standard Library**, meaning you do not need to install any external packages via pip. 

- **Python 3.6** or higher is required.

**Libraries Used:**
- `re` (Regular Expressions)
- `json` (Data formatting and export)
- `string` (Punctuation references)

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/TextProcessor.git
   cd TextProcessor
   ```

2. **Prepare your input file:**
   Create a text file named `input.txt` (or whatever you prefer) in the root directory and paste the text you want to analyze.

3. **Run the script:**
   ```bash
   python text_processor.py
   ```

---

## 💻 Usage Example

Here is a quick look at how the `TextProcessor` class works under the hood.

```python
from text_processor import TextProcessor

# Initialize the processor with your input file and desired output file name
processor = TextProcessor(file_path="input.txt", output_json="word_frequencies.json")

# Run the complete text processing pipeline
processor.process()
```

### Expected Input (`input.txt`)
```text
Hello world! Welcome to the world of Python. 
If you have questions, email us at contact@example.com or visit https://python.org.
```

### Expected Output (`word_frequencies.json`)
```json
{
    "Hello": 1,
    "world": 2,
    "Welcome": 1,
    "of": 1,
    "Python": 1,
    "If": 1,
    "you": 1,
    "have": 1,
    "questions": 1,
    "email": 1,
    "us": 1,
    "at": 1,
    "or": 1,
    "visit": 1
}
```

---

## 🏗️ Architecture & Pipeline Steps

The `TextProcessor.process()` method runs through a carefully orchestrated 6-step pipeline:

1. **`read_file()`**: Opens and reads the raw text from the specified file.
2. **`clean_text()`**: Applies Regex to strip URLs and emails, then removes standard punctuation.
3. **Tokenization**: Splits the cleaned string into an array of individual words.
4. **`remove_stopwords()`**: Filters the array against a `set` of predefined stop words to remove unhelpful terms.
5. **`count_word_frequencies()`**: Iterates through the filtered words and tallies their occurrences.
6. **`save_to_json()`**: Formats the final frequency dictionary and writes it to the designated `.json` output file.

---

## ⚙️ Customization

### Adding More Stop Words
You can easily expand the stop word list to fit your specific needs by modifying the `self.stop_words` set inside the `__init__` method.

```python
self.stop_words = set([
    "and", "in", "to", "from", "that", "this", "the", # ...
    "your_custom_word1", "your_custom_word2"          # Add new words here
])
```

### Case Sensitivity
By default, the script is **case-sensitive** (e.g., "Code" and "code" are counted as two different words). If you want to make it case-insensitive, you can modify the `clean_text` method to convert all text to lowercase before returning:

```python
def clean_text(self, text):
    # ... regex cleaning ...
    return text.lower()
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/TextProcessor/issues) if you want to contribute. 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
