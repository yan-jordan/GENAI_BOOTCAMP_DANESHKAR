# Task 3 — Embeddings & Vector Search (English + Persian)

A small, self-contained RAG/embedding playground that builds two parallel
similarity-search pipelines — one for English text, one for Persian text —
and compares how a local embedding model behaves versus a hosted one across
languages.

Everything lives in [`t3.ipynb`](./t3.ipynb).

## What it does

The notebook is split into two mirrored halves:

| | English pipeline | Persian pipeline |
|---|---|---|
| Document loader | `TextLoader` | `TextLoader` |
| Preprocessing | — | Normalized with `hazm.Normalizer` |
| Text splitter | `RecursiveCharacterTextSplitter` (default separators, `chunk_size=1000`, `chunk_overlap=100`) | `RecursiveCharacterTextSplitter` with Persian-aware separators (`\n\n`, `\n`, `؟ `, `! `, `. `, `، `, ` `), `chunk_size=1000`, `chunk_overlap=80` |
| Embedding model | OpenAI `text-embedding-3-small`, called through OpenRouter | Local `HooshvareLab/bert-base-parsbert-uncased` (Persian-finetuned BERT) via `langchain-huggingface`, run on CPU |
| Vector store | FAISS (`english_db`) | FAISS (`persian_db`) |
| Source data | `data/messi/messi.txt` | `data/messi/messi_persian.txt` |

A local `llama3.1:8b` model, served through Ollama and accessed via
`ChatOpenAI` pointed at Ollama's OpenAI-compatible endpoint
(`http://localhost:11434/v1`), is also wired up with streaming enabled as a
sanity check that the local LLM is reachable — it isn't otherwise part of
the retrieval pipeline.

Two separate FAISS databases are built because the two languages need two
different embedding models and two different splitters — a single shared
pipeline would either butcher Persian sentence boundaries or force Persian
text through an English-tuned embedding model, both of which hurt retrieval
quality.

## The most important gotcha: normalize the query too

Persian text needs Unicode/orthographic normalization (e.g. unifying
`ي`/`ی`, `ك`/`ک`, spacing around `‌` ZWNJ, etc.) before it's embedded, which
is why every Persian document is passed through:

```python
from hazm import Normalizer
n = Normalizer(persian_numbers=False)
persian_document.page_content = n.normalize(persian_document.page_content)
```

If a query string is embedded **without** running it through the same
`Normalizer` first, it can land in a different point of embedding space
than the (normalized) documents it should match, silently degrading
retrieval quality. The notebook normalizes the query before searching:

```python
query = n.normalize("مسی هشتمین توپ طلای رکوردشکن خود را چه زمانی برد")
response = persian_db.similarity_search(query=query)
```

**Rule of thumb: whatever preprocessing you apply to documents at index
time must also be applied to the query at search time.**

## Data

```
data/
├── messi/
│   ├── messi.txt              # ~2,700-word English biography of Lionel Messi
│   ├── messi_persian.txt      # faithful Persian translation of messi.txt
│   ├── messi_test.txt         # 20 Q&A pairs (English) for evaluating retrieval accuracy
│   └── messi_test_persian.txt # the same 20 Q&A pairs, in Persian
└── ai_risk/
    ├── ai_risk.txt             # ~5,300-word English article on AI risk
    └── ai_risk_persian.txt     # faithful Persian translation
```

The `messi` files are the ones currently wired into `t3.ipynb`. Both are
real, chronologically dense, name- and date-heavy text on purpose — good
stress test material for chunking and retrieval, since a right-vs-wrong
chunk match is easy to eyeball. The `messi_test*.txt` files exist so you can
sanity-check the search engine yourself: run a question through
`similarity_search`, and check whether the retrieved chunk actually
contains the paired answer.

The `ai_risk` pair is topically different (dense, discursive — thirteen
sections on different categories of AI risk rather than a chronological
narrative) and is included as a second, harder test corpus, but isn't yet
loaded into a cell in `t3.ipynb`.

## Setup

Requirements (already installed in the project's `venv`):

- `langchain`, `langchain-openai`, `langchain-community`, `langchain-huggingface`, `langchain-text-splitters`
- `faiss-cpu`
- `hazm` (Persian normalization)
- `torch`, `transformers`, `sentence-transformers` (backing the local HF embedding model)
- `python-dotenv`

External services:

- **Ollama** running locally with `llama3.1:8b` pulled (`ollama pull llama3.1:8b`, then `ollama serve`).
- An `OPENROUTER_API_KEY` in the project's `.env` file (used to call OpenAI's `text-embedding-3-small` via OpenRouter).

Select the `aibootcamp-venv` Jupyter kernel (registered from this project's
`venv`) when running the notebook — the default `python3` kernel points at
a different (Anaconda) environment that doesn't have these packages
installed.

## Running it

Run `t3.ipynb` top to bottom. It will:

1. Build the English FAISS index from `messi.txt` and persist it to `my_index/` via `english_db.save_local("my_index", "my_docs")`.
2. Build the Persian FAISS index from `messi_persian.txt` in memory (not currently persisted to disk).
3. Run one example query against each index and print the top matching chunk.

To evaluate retrieval quality more thoroughly, loop over the Q&A pairs in
`data/messi/messi_test.txt` / `messi_test_persian.txt`, run each question
through the matching `similarity_search`, and check whether the returned
chunk contains the paired answer.

## Known limitations / things to improve next

- The Persian FAISS index isn't persisted to disk yet (only the English one is).
- The `ai_risk` corpus is present but not yet loaded into the notebook — useful for testing retrieval on longer, less chronological text.
- Both pipelines currently use a single fixed `chunk_size`/`chunk_overlap`; no experimentation yet with how chunk size affects retrieval accuracy against the test Q&A sets.
