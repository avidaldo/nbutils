from pathlib import Path
from datetime import datetime
import nbformat

class JupyterManager:
    def __init__(self):
        self.supported_formats = {'.ipynb'}

    def list_notebooks(self, directory='.'):
        """List all Jupyter notebooks in the specified directory."""
        notebooks = []
        for file in Path(directory).rglob('*.ipynb'):
            if file.suffix in self.supported_formats:
                notebooks.append({
                    'path': str(file),
                    'name': file.name,
                    'last_modified': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        return notebooks

    def get_notebook_info(self, notebook_path):
        """Get detailed information about a specific notebook."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            
        cell_count = {
            'code': len([c for c in nb.cells if c.cell_type == 'code']),
            'markdown': len([c for c in nb.cells if c.cell_type == 'markdown']),
            'raw': len([c for c in nb.cells if c.cell_type == 'raw'])
        }
        
        return {
            'filename': Path(notebook_path).name,
            'cell_count': cell_count,
            'kernel_spec': nb.metadata.get('kernelspec', {}),
            'total_cells': len(nb.cells)
        }

    def clear_notebook_outputs(self, notebook_path):
        """Clear all output cells in a notebook."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        for cell in nb.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)