"""Core NBUtils class for notebook operations."""

import json
from pathlib import Path

from .operations.convert import notebook_to_markdown, notebook_to_py, py_to_notebook
from .operations.headings import adjust_file_headings


class NBUtils:
    """Main utility class for notebook operations."""
    
    def __init__(self, input_path: str | None = None):
        self.input_path = input_path
        
    def convert_to_markdown(self, output_path: str | None = None) -> str:
        """Convert notebook to markdown"""
        with open(self.input_path, 'r', encoding='utf-8') as f:
            notebook_content = json.load(f)
            
        markdown_content = notebook_to_markdown(notebook_content)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        return markdown_content

    def convert_to_py(self, output_path: str | None = None) -> str:
        """Convert notebook to Python file"""
        with open(self.input_path, 'r', encoding='utf-8') as f:
            notebook_content = json.load(f)
            
        py_content = notebook_to_py(notebook_content)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(py_content)
        return py_content

    def adjust_headings(self, increase: bool, force: bool = False) -> None:
        """Adjust heading levels in the notebook.
        
        Args:
            increase: True to increase heading levels, False to decrease
            force: If True, proceed even with first-level headings when decreasing
        """
        result = adjust_file_headings(self.input_path, increase, force)
        if not result.success:
            raise ValueError(result.error or "Failed to adjust headings")
        
    def convert_from_py(self, output_path: str | None = None) -> dict[str, any]:
        """Convert Python file to Jupyter notebook"""
        with open(self.input_path, 'r', encoding='utf-8') as f:
            py_content = f.read()
            
        notebook_content = py_to_notebook(py_content)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(notebook_content, f, indent=2)
        return notebook_content