# NBUtils

A command-line utility for managing and converting Jupyter notebooks.

## Features

- Convert between different formats:
  - Jupyter Notebook (.ipynb) to Markdown (.md)
  - Jupyter Notebook (.ipynb) to Python (.py)
  - Python (.py) to Jupyter Notebook (.ipynb)
  - Markdown (.md) to Python (.py)
  - Markdown (.md) to Jupyter Notebook (.ipynb) (not implemented yet)

- Batch convert all notebooks in a directory to markdown files
(ideal for uploading to NotebookLM)

- Batch convert all Python files in a directory to Jupyter notebooks
(converts comments to markdown cells and code to code cells)

- Increase or decrease all titles in a markdown file (or notebook)

## Installation

```bash
git clone https://github.com/avidaldo/nbutils
cd nbutils
pip install .
```

## Usage

```bash
# Convert markdown to notebook
nbu convert input.md output.ipynb

# Convert notebook to python
nbu convert input.ipynb output.py

# Convert python to notebook
nbu convert input.py output.ipynb

# Convert markdown to python
nbu convert input.md output.py

# Create a directory with all notebooks in the current directory as markdown files
nbu batch-md

# Create a directory with all Python files in the current directory as Jupyter notebooks
nbu batch-ipynb

# Increase all headings in a markdown file
nbu increase-headings +

# Decrease all headings in a markdown file
nbu increase-headings -

```

