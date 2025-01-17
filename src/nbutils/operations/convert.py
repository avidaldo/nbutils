from typing import Dict, Any

def notebook_to_markdown(notebook_content: Dict[str, Any]) -> str:
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

def notebook_to_py(notebook_content: Dict[str, Any]) -> str:
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