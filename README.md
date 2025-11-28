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

- Increase or decrease all headings in markdown files or notebooks
  - Supports multiple files at once
  - Interactive warnings when decreasing first-level headings

## Installation

```bash
git clone https://github.com/avidaldo/nbutils
cd nbutils
pipx install .
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

# Increase all headings in a file (notebook or markdown)
nbu inc-heads file.ipynb

# Increase headings in multiple files
nbu inc-heads file1.ipynb file2.md file3.ipynb

# Decrease all headings in a file (notebook or markdown)
nbu dec-heads file.md

# Decrease headings in multiple files
nbu dec-heads file1.ipynb file2.md

# Force decrease even with first-level headings (skip confirmation)
nbu dec-heads -f file.ipynb
 

```

