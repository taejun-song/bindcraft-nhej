"""
Entry point for BindCraft NHEJ package.

This module serves as a simple entry point for the package.
For CLI usage, use the `bindcraft-nhej` command installed with the package.
"""

from bindcraft_nhej.cli.main import cli


def main():
    """Main entry point for the package."""
    print("BindCraft NHEJ - Protein binder design using non-homologous end joining")
    print("Use 'bindcraft-nhej --help' for command line interface")
    print("Or import bindcraft_nhej in Python for programmatic access")


if __name__ == "__main__":
    # If running this script directly, show the CLI
    cli()
