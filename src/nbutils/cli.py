"""Command-line interface for NBUtils."""

from pathlib import Path

import click

from .core import NBUtils
from .operations.headings import adjust_file_headings


def find_notebooks(path: str = '.') -> list[str]:
    """Find all Jupyter notebooks in the given path."""
    return [str(p) for p in Path(path).rglob('*.ipynb')]


def find_python_files(path: str = '.') -> list[str]:
    """Find all Python files in the given path."""
    return [str(p) for p in Path(path).rglob('*.py')]


def get_output_path(input_path: str, output_dir: str, extension: str) -> str:
    """Convert input path to output path in the specified output directory.
    
    Example: 'path/to/notebook.ipynb' -> 'output_dir/path_to_notebook.md'
    """
    # Convert path to relative if it's absolute
    rel_path = Path(input_path).relative_to(Path.cwd()) if Path(input_path).is_absolute() else Path(input_path)
    # Remove extension and replace path separators with underscores
    base_name = str(rel_path.with_suffix('')).replace('/', '_').replace('\\', '_')
    # Create output path
    return str(Path(output_dir) / f"{base_name}{extension}")


@click.group()
def cli():
    """Notebook utilities CLI."""
    pass


@cli.command('convert')
@click.argument('input_path')
@click.argument('output_path')
def convert(input_path: str, output_path: str):
    """Convert between notebook, markdown, and python formats."""
    try:
        if input_path.endswith('.ipynb'):
            # Convert notebook to markdown or python
            if output_path.endswith('.md'):
                nb = NBUtils(input_path)
                nb.convert_to_markdown(output_path)
                click.echo(f"✓ Converted {input_path} → {output_path}")
            elif output_path.endswith('.py'):
                nb = NBUtils(input_path)
                nb.convert_to_py(output_path)
                click.echo(f"✓ Converted {input_path} → {output_path}")
            else:
                click.echo("✗ Unsupported output format. Use .md or .py.")
        elif input_path.endswith('.md'):
            # Convert markdown to notebook or python
            if output_path.endswith('.ipynb'):
                click.echo("✗ Markdown to notebook conversion not implemented.")
            elif output_path.endswith('.py'):
                click.echo("✗ Markdown to python conversion not implemented.")
            else:
                click.echo("✗ Unsupported output format. Use .ipynb or .py.")
        elif input_path.endswith('.py'):
            # Convert Python to notebook
            if output_path.endswith('.ipynb'):
                nb = NBUtils(input_path)
                nb.convert_from_py(output_path)
                click.echo(f"✓ Converted {input_path} → {output_path}")
            else:
                click.echo("✗ Unsupported output format for Python input. Use .ipynb.")
        else:
            click.echo("✗ Unsupported input format. Use .ipynb, .md, or .py.")
    except Exception as e:
        click.echo(f"✗ Failed to convert {input_path} to {output_path}: {str(e)}")


@cli.command('batch-md')
@click.argument('path', default='.')
@click.option('-o', '--output-dir', default='markdown', help='Output directory for markdown files')
def batch_to_markdown(path: str, output_dir: str):
    """Convert all notebooks in path to markdown."""
    notebooks = find_notebooks(path)
    click.echo(f"Found {len(notebooks)} notebook(s). Converting to markdown...")
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for nb_path in notebooks:
        try:
            md_path = get_output_path(nb_path, output_dir, '.md')
            nb = NBUtils(nb_path)
            nb.convert_to_markdown(md_path)
            click.echo(f"✓ Converted {nb_path} → {md_path}")
        except Exception as e:
            click.echo(f"✗ Failed to convert {nb_path}: {str(e)}")


@cli.command('batch-py')
@click.argument('path', default='.')
@click.option('-o', '--output-dir', default='python', help='Output directory for Python files')
def batch_to_python(path: str, output_dir: str):
    """Convert all notebooks in path to Python files."""
    notebooks = find_notebooks(path)
    click.echo(f"Found {len(notebooks)} notebook(s). Converting to Python...")
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for nb_path in notebooks:
        try:
            py_path = get_output_path(nb_path, output_dir, '.py')
            nb = NBUtils(nb_path)
            nb.convert_to_py(py_path)
            click.echo(f"✓ Converted {nb_path} → {py_path}")
        except Exception as e:
            click.echo(f"✗ Failed to convert {nb_path}: {str(e)}")


@cli.command('batch-ipynb')
@click.argument('path', default='.')
@click.option('-o', '--output-dir', default='notebooks', help='Output directory for Jupyter notebooks')
def batch_to_notebook(path: str, output_dir: str):
    """Convert all Python files in path to Jupyter notebooks."""
    py_files = find_python_files(path)
    click.echo(f"Found {len(py_files)} Python file(s). Converting to Jupyter notebooks...")
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for py_path in py_files:
        try:
            ipynb_path = get_output_path(py_path, output_dir, '.ipynb')
            nb = NBUtils(py_path)
            nb.convert_from_py(ipynb_path)
            click.echo(f"✓ Converted {py_path} → {ipynb_path}")
        except Exception as e:
            click.echo(f"✗ Failed to convert {py_path}: {str(e)}")


@cli.command('inc-heads')
@click.argument('files', nargs=-1, required=True)
def increase_headings(files: tuple[str, ...]):
    """Increase heading levels in notebooks or markdown files.
    
    Accepts multiple file paths. Supports both .ipynb and .md files.
    
    Examples:
        nbu inc-heads file1.ipynb file2.md file3.ipynb
    """
    if not files:
        click.echo("✗ No files specified.")
        return
    
    for file_path in files:
        try:
            result = adjust_file_headings(file_path, increase=True)
            if result.success:
                click.echo(f"✓ Increased headings in {file_path}")
            else:
                click.echo(f"✗ Failed to update {file_path}: {result.error}")
        except Exception as e:
            click.echo(f"✗ Failed to update {file_path}: {str(e)}")


@cli.command('dec-heads')
@click.argument('files', nargs=-1, required=True)
@click.option('-f', '--force', is_flag=True, help='Force decrease even with first-level headings')
def decrease_headings(files: tuple[str, ...], force: bool):
    """Decrease heading levels in notebooks or markdown files.
    
    Accepts multiple file paths. Supports both .ipynb and .md files.
    
    If first-level headings are detected, a warning will be shown and you'll
    be asked for confirmation unless --force is used.
    
    Examples:
        nbu dec-heads file1.ipynb file2.md
        nbu dec-heads -f file1.ipynb  # Force without confirmation
    """
    if not files:
        click.echo("✗ No files specified.")
        return
    
    # First pass: check all files for first-level headings
    files_with_warnings = []
    for file_path in files:
        try:
            result = adjust_file_headings(file_path, increase=False, force=False)
            if not result.success and result.warnings:
                files_with_warnings.append((file_path, result.warnings))
        except Exception as e:
            click.echo(f"✗ Failed to check {file_path}: {str(e)}")
            return
    
    # If we have warnings and not forcing, ask for confirmation
    if files_with_warnings and not force:
        click.echo("\n⚠ Warning: The following files contain first-level headings:")
        for file_path, warnings in files_with_warnings:
            click.echo(f"  • {file_path}")
            for warning in warnings:
                click.echo(f"    - {warning}")
        
        click.echo("\nDecreasing first-level headings will convert them to non-heading text.")
        if not click.confirm("Do you want to proceed anyway?"):
            click.echo("Operation cancelled.")
            return
        
        # User confirmed, set force to True for processing
        force = True
    
    # Process all files
    for file_path in files:
        try:
            result = adjust_file_headings(file_path, increase=False, force=force)
            if result.success:
                click.echo(f"✓ Decreased headings in {file_path}")
                if result.warnings:
                    for warning in result.warnings:
                        click.echo(f"  ⚠ {warning}")
            else:
                click.echo(f"✗ Failed to update {file_path}: {result.error}")
        except Exception as e:
            click.echo(f"✗ Failed to update {file_path}: {str(e)}")


if __name__ == '__main__':
    cli()