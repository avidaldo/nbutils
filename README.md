# NBUtils

A command-line utility for managing and converting Jupyter notebooks.

## Features

- Convert between different formats:
  - Jupyter Notebook (.ipynb) to Markdown (.md)
  - Markdown (.md) to Jupyter Notebook (.ipynb)
  - Jupyter Notebook (.ipynb) to Python (.py)
  - Markdown (.md) to Python (.py)

- Batch convert all notebooks in a directory to markdown files
(ideal for uploading to NotebookLM)

- Increase or decrease all titles in a markdown file (or notebook)

## Installation

```bash
git clone https://github.com/avidaldo/nbutils
cd nbutils
pip install nbutils
```

## Usage

```bash
# Convert markdown to notebook
nbu convert input.md output.ipynb

# Convert notebook to python
nbu convert input.ipynb output.py

# Convert markdown to python
nbu convert input.md output.py

# Create a directory with all notebooks in the current directory as markdown files
nbu batch-md

# Increase all headings in a markdown file
nbu increase-headings +

# Decrease all headings in a markdown file
nbu increase-headings -

```

