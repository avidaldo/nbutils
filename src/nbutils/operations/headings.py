import os
import json
from typing import Literal

def adjust_headings(notebook_path: str, adjustment: Literal['+', '-']) -> None:
    """
    Adjust heading levels in a Jupyter notebook.
    
    Args:
        notebook_path: Path to the notebook file
        adjustment: '+' to increase heading levels, '-' to decrease
    """
    # Check if the file exists
    if not os.path.isfile(notebook_path):
        print(f"Error: File {notebook_path} does not exist.")
        return

    # Check if the adjustment parameter is valid
    if adjustment not in ['-', '+']:
        print("Error: Adjustment parameter must be '+' or '-'.")
        return

    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            source = cell['source']
            if isinstance(source, str):
                lines = source.split('\n')
            else:
                lines = source

            for i, line in enumerate(lines):
                if line.startswith('#'):
                    if adjustment == '-' and line.startswith('# '):
                        print(f"Error: Cannot reduce first-level heading in line {i+1}")
                        return
                    elif adjustment == '+':
                        lines[i] = '#' + line
                    elif adjustment == '-':
                        lines[i] = line[1:] if line.startswith('##') else line
            
            cell['source'] = lines if isinstance(source, list) else '\n'.join(lines)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False)