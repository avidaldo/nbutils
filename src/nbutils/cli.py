import os
import glob
import click
from typing import List
from pathlib import Path

from .core import NBUtils

def find_notebooks(path: str = '.') -> List[str]:
    """Find all Jupyter notebooks in the given path"""
    return glob.glob(os.path.join(path, '**/*.ipynb'), recursive=True)

def get_output_path(input_path: str, output_dir: str, extension: str) -> str:
    """
    Convert input path to output path in the specified output directory.
    Example: 'path/to/notebook.ipynb' -> 'output_dir/path_to_notebook.md'
    """
    # Convert path to relative if it's absolute
    rel_path = os.path.relpath(input_path)
    # Remove extension and replace path separators with underscores
    base_name = os.path.splitext(rel_path)[0].replace(os.sep, '_')
    # Create output path
    return os.path.join(output_dir, f"{base_name}{extension}")

@click.group()
def cli():
    """Notebook utilities CLI"""
    pass

@cli.command('batch-md')
@click.argument('path', default='.')
@click.option('-o', '--output-dir', default='markdown', help='Output directory for markdown files')
def batch_to_markdown(path: str, output_dir: str):
    """Convert all notebooks in path to markdown"""
    notebooks = find_notebooks(path)
    click.echo(f"Found {len(notebooks)} notebook(s). Converting to markdown...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for nb_path in notebooks:
        try:
            md_path = get_output_path(nb_path, output_dir, '.md')
            nb = NBUtils(nb_path)
            nb.convert_to_markdown(md_path)
            click.echo(f"✓ Converted {nb_path} -> {md_path}")
        except Exception as e:
            click.echo(f"✗ Failed to convert {nb_path}: {str(e)}")

@cli.command('batch-py')
@click.argument('path', default='.')
@click.option('-o', '--output-dir', default='python', help='Output directory for Python files')
def batch_to_python(path: str, output_dir: str):
    """Convert all notebooks in path to Python files"""
    notebooks = find_notebooks(path)
    click.echo(f"Found {len(notebooks)} notebook(s). Converting to Python...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for nb_path in notebooks:
        try:
            py_path = get_output_path(nb_path, output_dir, '.py')
            nb = NBUtils(nb_path)
            nb.convert_to_py(py_path)
            click.echo(f"✓ Converted {nb_path} -> {py_path}")
        except Exception as e:
            click.echo(f"✗ Failed to convert {nb_path}: {str(e)}")

@cli.command('adjust-headings')
@click.argument('path')
@click.option('-a', '--adjustment', type=click.Choice(['+', '-']), required=True,
              help='Increase (+) or decrease (-) heading levels')
def adjust_headings(path: str, adjustment: str):
    """Adjust heading levels in notebooks"""
    if os.path.isfile(path):
        notebooks = [path]
    else:
        notebooks = find_notebooks(path)
    
    click.echo(f"Found {len(notebooks)} notebook(s). Adjusting headings...")
    
    for nb_path in notebooks:
        try:
            nb = NBUtils(nb_path)
            nb.adjust_headings(adjustment)
            click.echo(f"✓ Updated {nb_path}")
        except Exception as e:
            click.echo(f"✗ Failed to update {nb_path}: {str(e)}")

if __name__ == '__main__':
    cli()