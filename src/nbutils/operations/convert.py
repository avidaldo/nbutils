"""Operations for converting between Jupyter notebooks, Python files, and markdown."""


def notebook_to_markdown(notebook_content: dict[str, any]) -> str:
    """Convert Jupyter notebook to markdown format"""
    markdown_lines = []
    
    for cell in notebook_content['cells']:
        source = cell['source']
        if isinstance(source, list):
            source = ''.join(source)
            
        if cell['cell_type'] == 'markdown':
            markdown_lines.append(source)
            markdown_lines.append('')
        elif cell['cell_type'] == 'code':
            markdown_lines.append('```python')
            markdown_lines.append(source)
            markdown_lines.append('```')
            markdown_lines.append('')
            
    return '\n'.join(markdown_lines)

def notebook_to_py(notebook_content: dict[str, any]) -> str:
    """Convert Jupyter notebook to Python file with markdown as comments"""
    py_lines = []
    
    for cell in notebook_content['cells']:
        source = cell['source']
        if isinstance(source, list):
            source = ''.join(source)
            
        if cell['cell_type'] == 'markdown':
            for line in source.split('\n'):
                if line.strip():
                    if line.startswith('#'):
                        py_lines.append(f"#{line}")
                    else:
                        py_lines.append(f"# {line}")
                else:
                    py_lines.append('')
        elif cell['cell_type'] == 'code':
            py_lines.append(source)
            py_lines.append('')
            
    return '\n'.join(py_lines)

def py_to_notebook(py_content: str) -> dict[str, any]:
    """Convert Python file to Jupyter notebook format
    
    Parses a Python file and converts it to a Jupyter notebook by:
    - Converting code blocks to code cells
    - Converting comment blocks to markdown cells
    """
    # Create basic notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    lines = py_content.splitlines()
    current_block = []
    current_type = None
    
    # Helper function to add the current block as a cell
    def add_current_block():
        nonlocal current_block, current_type
        if not current_block:
            return
            
        if current_type == "code":
            notebook["cells"].append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + "\n" for line in current_block]
            })
        elif current_type == "markdown":
            # Convert Python comments to markdown
            markdown_lines = []
            for line in current_block:
                if line.startswith("# "):
                    markdown_lines.append(line[2:])
                elif line.startswith("#"):
                    markdown_lines.append(line[1:])
                else:
                    markdown_lines.append(line)
                    
            notebook["cells"].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + "\n" for line in markdown_lines]
            })
            
        current_block = []
        current_type = None
    
    # Process each line
    for line in lines:
        # Detect if this is a comment or code line
        is_comment = line.strip().startswith("#") or not line.strip()
        line_type = "markdown" if is_comment else "code"
        
        # If we're switching between comment and code, add the current block as a cell
        if current_type and current_type != line_type:
            add_current_block()
            
        current_type = line_type
        current_block.append(line)
    
    # Add the final block
    add_current_block()
    
    return notebook 