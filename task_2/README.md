# Task 2 — Prompt Engineering Experiments

A notebook ([`project2.ipynb`](./project2.ipynb)) exploring how prompt
structure and prompting strategy change an LLM's output, using LangChain
against `google/gemma-4-26b-a4b-it:free` served through OpenRouter.

## What it does

The notebook is organized into three experiments, all built around the
same research subject: *"AI's impact on employees' lives in the next few
years."*

### 1. Three levels of prompt detail

The same underlying request — "write a paper on AI's impact on employees'
lives" — is sent to the model at three levels of detail, to compare output
quality:

| Level | Prompt style | What it produces |
|---|---|---|
| 1 | One vague sentence, no structure | A short, generic paper |
| 2 | A bullet list of required sections (introduction, pros/cons, challenges, solutions, conclusion, sources) | A more complete, structured paper |
| 3 | A fully specified prompt: assigns the model a persona ("professional academic researcher"), lists every required section in detail, and explicitly asks for anything useful the prompt didn't already cover | The most thorough and well-organized paper of the three |

This is a direct, side-by-side demonstration of how much prompt
specificity affects output quality, using `PromptTemplate` for each level.

### 2. Zero-shot vs. few-shot prompting (tone control)

The level-3 research paper from experiment 1 is fed back in as input to a
summarization task: *"summarize this research in 2 sentences in a
`{tone}` tone."*

- **Zero-shot:** just the instruction and the tone variable, no examples.
- **Few-shot:** the same instruction, preceded by three `FewShotChatMessagePromptTemplate`
  examples that each rewrite a dry scientific fact (the human microbiome,
  emergent behavior in neural nets, quantum entanglement) into
  deliberately over-the-top horror-movie prose.

Asking for `tone = "scary and horror"` shows the few-shot version
committing much harder to the requested tone than the zero-shot version,
because the examples give the model concrete stylistic targets to
pattern-match against rather than just an adjective to interpret.

### 3. Structured extraction: zero-shot vs. few-shot

A synthetic resume (`sample_resume_1`, a fictional ML engineer) is passed
to the model with two different prompting strategies:

- **Zero-shot:** `"extract data from this resume: {resume}"` — no schema,
  no example of what "extracted data" should look like.
- **Few-shot:** a `FewShotChatMessagePromptTemplate` built from two more
  synthetic resume/JSON pairs (`sample_resume_2` / `sample_resume_3`,
  fictional marketing and backend-engineering candidates), each paired
  with a target JSON extraction, followed by `sample_resume_1` as the real
  input.

The few-shot version produces output that reliably follows a consistent
JSON shape, since the examples demonstrate the exact schema (candidate
info, tech stack, work history, education, certs, etc.) rather than
leaving the model to invent its own structure.

## Setup

- `langchain`, `langchain-openai`, `langchain-core`, `python-dotenv`
- An `OPENROUTER_API_KEY` in the project's `.env` file (used as the
  `api_key` for `ChatOpenAI`, pointed at
  `https://openrouter.ai/api/v1` with `model_name="google/gemma-4-26b-a4b-it:free"`)

## Running it

Run `project2.ipynb` top to bottom. Each experiment's markdown cell
documents which prompting level or strategy the cell below it is testing,
and the LLM output is printed directly below each code cell so you can
compare results as you go.

## Known Issues

- **The few-shot resume examples are cross-labeled.** In the final cell,
  `sample_resume_2_output` actually contains the extracted JSON for the
  *`sample_resume_3`* candidate (Amara Okafor), and `sample_resume_3_output`
  contains the extracted JSON for the *`sample_resume_2`* candidate (David
  Chen) — the two output variables are swapped relative to their matching
  input resumes. Since `resume_examples` pairs each input with its
  (mismatched) output, the few-shot examples currently teach the model an
  incorrect input → output correspondence. Swap the two `_output`
  assignments (or rename the variables) before drawing conclusions from
  that cell's results.
