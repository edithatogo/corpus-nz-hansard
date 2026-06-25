#!/usr/bin/env python
"""Profile the Hansard normalization, PDF/text handling, and Parquet rebuild pipelines."""

import cProfile
import pstats
import io
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console

console = Console()

# Base directory for this repo
BASE_DIR = Path(__file__).parent.parent


def profile_normalize_hansard():
    """Profile the normalize_hansard script."""
    console.print("[bold cyan]Profiling normalize_hansard...[/bold cyan]")

    # Check if there's test data
    test_data_dir = BASE_DIR / "generated" / "parquet"
    if not test_data_dir.exists():
        console.print("[yellow]No test data found in generated/parquet, skipping[/yellow]")
        return

    profiler = cProfile.Profile()
    profiler.enable()

    # Import and run the main function
    try:
        from normalize_hansard import main as normalize_main

        # This would need actual args - for now just import test
        console.print("[yellow]normalize_hansard imported (full run requires CLI args)[/yellow]")
    except ImportError as e:
        console.print(f"[red]Could not import normalize_hansard: {e}[/red]")

    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(30)
    console.print(s.getvalue())

    output_path = BASE_DIR / "logs" / "profile_normalize_hansard.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(s.getvalue())
    console.print(f"[green]Profile saved to {output_path}[/green]")


def profile_build_parquet():
    """Profile the build_duckdb / parquet building scripts."""
    console.print("[bold cyan]Profiling parquet building...[/bold cyan]")

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        from build_duckdb import main as build_duckdb_main

        console.print("[yellow]build_duckdb imported (full run requires CLI args)[/yellow]")
    except ImportError as e:
        console.print(f"[red]Could not import build_duckdb: {e}[/red]")

    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(30)
    console.print(s.getvalue())

    output_path = BASE_DIR / "logs" / "profile_build_parquet.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(s.getvalue())
    console.print(f"[green]Profile saved to {output_path}[/green]")


def profile_pdf_handling():
    """Profile PDF/text handling (pdfplumber, pypdf usage)."""
    console.print("[bold cyan]Profiling PDF handling imports...[/bold cyan]")

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        import pdfplumber
        import pypdf

        console.print("[green]pdfplumber and pypdf imported successfully[/green]")
    except ImportError as e:
        console.print(f"[red]Could not import PDF libraries: {e}[/red]")

    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.print_stats(30)
    console.print(s.getvalue())

    output_path = BASE_DIR / "logs" / "profile_pdf_handling.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(s.getvalue())
    console.print(f"[green]Profile saved to {output_path}[/green]")


def main():
    """Run all profiling tasks."""
    console.print("[bold]Starting corpus-nz-hansard profiling[/bold]")

    # Ensure logs directory exists
    (BASE_DIR / "logs").mkdir(exist_ok=True)

    # Run profiles
    profile_normalize_hansard()
    profile_build_parquet()
    profile_pdf_handling()

    console.print("[bold green]Profiling complete![/bold green]")


if __name__ == "__main__":
    main()
