"""
Demo: Text Enhancement
Usage: python demos/text_enhance.py --source 0 --show
"""
import sys
import os
from pathlib import Path

# Add src to path if running directly
sys.path.append(str(Path(__file__).parent.parent / "src"))

from vademos.cli import text_enhance
from typer.testing import CliRunner

if __name__ == "__main__":
    # Just invoke the CLI command directly
    import typer
    typer.run(text_enhance)
