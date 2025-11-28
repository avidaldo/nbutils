"""Operations for adjusting heading levels in Jupyter notebooks and markdown files."""

from pathlib import Path
from dataclasses import dataclass

import nbformat
from nbformat.notebooknode import NotebookNode


@dataclass
class HeadingAdjustmentResult:
    """Result of a heading adjustment operation."""
    success: bool
    warnings: list[str]
    error: str | None = None


def _adjust_heading_line(line: str, increase: bool) -> str:
    """Adjust a single heading line.
    
    Args:
        line: The line to adjust
        increase: True to increase heading level (add #), False to decrease
        
    Returns:
        The adjusted line
    """
    if not line.startswith('#'):
        return line
    
    if increase:
        return '#' + line
    else:
        # Decrease: remove one #
        if line.startswith('## '):
            return line[1:]
        elif line.startswith('#'):
            # For single # or #without space, just remove one
            return line[1:]
        return line


def _has_first_level_heading(source: str | list[str]) -> bool:
    """Check if markdown source contains first-level headings.
    
    Args:
        source: Markdown source as string or list of strings
        
    Returns:
        True if source contains '# ' at the start of any line
    """
    if isinstance(source, str):
        lines = source.split('\n')
    else:
        lines = source
    
    return any(line.startswith('# ') for line in lines)


def _adjust_markdown_source(source: str | list[str], increase: bool) -> str | list[str]:
    """Adjust heading levels in markdown source.
    
    Args:
        source: Markdown source as string or list of strings
        increase: True to increase heading level, False to decrease
        
    Returns:
        Adjusted source in the same format as input
    """
    is_list = isinstance(source, list)
    lines = source if is_list else source.split('\n')
    
    adjusted_lines = [_adjust_heading_line(line, increase) for line in lines]
    
    return adjusted_lines if is_list else '\n'.join(adjusted_lines)


def adjust_notebook_headings(
    notebook_path: str | Path,
    increase: bool,
    force: bool = False
) -> HeadingAdjustmentResult:
    """Adjust heading levels in a Jupyter notebook.
    
    Args:
        notebook_path: Path to the notebook file
        increase: True to increase heading levels, False to decrease
        force: If True, proceed even with first-level headings when decreasing
        
    Returns:
        HeadingAdjustmentResult with status and any warnings
    """
    notebook_path = Path(notebook_path)
    
    if not notebook_path.exists():
        return HeadingAdjustmentResult(
            success=False,
            warnings=[],
            error=f"File {notebook_path} does not exist"
        )
    
    try:
        # Read notebook using nbformat
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
    except Exception as e:
        return HeadingAdjustmentResult(
            success=False,
            warnings=[],
            error=f"Failed to read notebook: {str(e)}"
        )
    
    warnings = []
    
    # Check for first-level headings if decreasing
    if not increase and not force:
        for cell in notebook.cells:
            if cell.cell_type == 'markdown':
                if _has_first_level_heading(cell.source):
                    warnings.append(
                        "Found first-level heading(s). Decreasing will result in non-heading text."
                    )
                    break
    
    # If we found warnings and not forcing, return without modifying
    if warnings and not force:
        return HeadingAdjustmentResult(
            success=False,
            warnings=warnings,
            error=None
        )
    
    # Adjust headings in all markdown cells
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            cell.source = _adjust_markdown_source(cell.source, increase)
    
    # Write back using nbformat
    try:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)
    except Exception as e:
        return HeadingAdjustmentResult(
            success=False,
            warnings=warnings,
            error=f"Failed to write notebook: {str(e)}"
        )
    
    return HeadingAdjustmentResult(
        success=True,
        warnings=warnings,
        error=None
    )


def adjust_markdown_headings(
    markdown_path: str | Path,
    increase: bool,
    force: bool = False
) -> HeadingAdjustmentResult:
    """Adjust heading levels in a markdown file.
    
    Args:
        markdown_path: Path to the markdown file
        increase: True to increase heading levels, False to decrease
        force: If True, proceed even with first-level headings when decreasing
        
    Returns:
        HeadingAdjustmentResult with status and any warnings
    """
    markdown_path = Path(markdown_path)
    
    if not markdown_path.exists():
        return HeadingAdjustmentResult(
            success=False,
            warnings=[],
            error=f"File {markdown_path} does not exist"
        )
    
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return HeadingAdjustmentResult(
            success=False,
            warnings=[],
            error=f"Failed to read markdown file: {str(e)}"
        )
    
    warnings = []
    
    # Check for first-level headings if decreasing
    if not increase and not force:
        if _has_first_level_heading(content):
            warnings.append(
                "Found first-level heading(s). Decreasing will result in non-heading text."
            )
    
    # If we found warnings and not forcing, return without modifying
    if warnings and not force:
        return HeadingAdjustmentResult(
            success=False,
            warnings=warnings,
            error=None
        )
    
    # Adjust headings
    adjusted_content = _adjust_markdown_source(content, increase)
    
    # Write back
    try:
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(adjusted_content)
    except Exception as e:
        return HeadingAdjustmentResult(
            success=False,
            warnings=warnings,
            error=f"Failed to write markdown file: {str(e)}"
        )
    
    return HeadingAdjustmentResult(
        success=True,
        warnings=warnings,
        error=None
    )


def adjust_file_headings(
    file_path: str | Path,
    increase: bool,
    force: bool = False
) -> HeadingAdjustmentResult:
    """Adjust heading levels in a notebook or markdown file.
    
    Args:
        file_path: Path to the file (.ipynb or .md)
        increase: True to increase heading levels, False to decrease
        force: If True, proceed even with first-level headings when decreasing
        
    Returns:
        HeadingAdjustmentResult with status and any warnings
    """
    file_path = Path(file_path)
    
    if file_path.suffix == '.ipynb':
        return adjust_notebook_headings(file_path, increase, force)
    elif file_path.suffix == '.md':
        return adjust_markdown_headings(file_path, increase, force)
    else:
        return HeadingAdjustmentResult(
            success=False,
            warnings=[],
            error=f"Unsupported file type: {file_path.suffix}. Use .ipynb or .md"
        )