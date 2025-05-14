
# General Inquiry Sample using searching and crawling

This is a sample of using the `query-rewrite` technique for a user's question, creating a keyword for search and a question for LLM, then performing a search using the keyword for search, crawling the top n sites, and asking the question to LLM to generate an answer.

## Features

- Query Rewriting: Rewrite the user's question to create a keyword for search and a question for LLM.
- Search: Perform a search using the keyword for search.
- Crawl: Crawl the top n sites from the search results.
- Ask LLM: Ask the question to LLM to generate an answer.

## Get Started

### Prerequisites

- Python 3.12
- uv   
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create a virtual environment and install dependencies

```bash

uv venv .venv --python 3.12 --seed
source .venv/bin/activate
uv pip install -r pyproject.toml

```

### Set up environment variables

```bash
cp .env.example .env
```

- Set each environment variable in `.env` file.

### Open the notebook

[notebook](./llm_websearch_crawlingn.ipynb)


## TODO

- [x] Make crawler aync
- [ ] Refine prompt
- [ ] Change to use Function Calling
- [ ] Experiment Azure AI Agent to compare latency and quality