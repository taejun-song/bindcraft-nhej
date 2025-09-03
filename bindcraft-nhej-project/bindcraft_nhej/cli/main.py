"""Command line interface for BindCraft NHEJ."""

import click
import os
from typing import Optional

from bindcraft_nhej.core.config import Settings, create_default_settings
from bindcraft_nhej.core.binder_design import BinderDesigner


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """BindCraft NHEJ - Protein binder design using non-homologous end joining."""
    pass


@cli.command()
@click.option('--design-path', help='Path to save designs')
@click.option('--binder-name', help='Name prefix for binders')
@click.option('--starting-pdb', help='Path to target PDB structure')
@click.option('--chains', default='A', help='Target chains (comma-separated)')
@click.option('--target-hotspot-residues', default='', help='Target hotspot residues')
@click.option('--min-length', default=30, help='Minimum binder length')
@click.option('--max-length', default=110, help='Maximum binder length') 
@click.option('--number-of-designs', default=2, help='Number of final designs required')
@click.option('--config', help='Load configuration from JSON file')
def design(
    design_path: Optional[str],
    binder_name: Optional[str],
    starting_pdb: Optional[str],
    chains: str,
    target_hotspot_residues: str,
    min_length: int,
    max_length: int,
    number_of_designs: int,
    config: Optional[str]
):
    """Run binder design with specified parameters."""
    
    if config:
        if not os.path.exists(config):
            click.echo(f"Error: Configuration file {config} not found", err=True)
            return
        # Load from config file
        settings = Settings.load(config)
        click.echo(f"Loaded configuration from {config}")
    else:
        # Validate required parameters when no config file
        missing = []
        if not design_path:
            missing.append('--design-path')
        if not binder_name:
            missing.append('--binder-name') 
        if not starting_pdb:
            missing.append('--starting-pdb')
            
        if missing:
            click.echo(f"Error: Missing required options: {', '.join(missing)}", err=True)
            click.echo("Either provide --config or all required parameters", err=True)
            return
            
        # Create from command line arguments
        settings = create_default_settings(
            design_path=design_path,
            binder_name=binder_name,
            starting_pdb=starting_pdb,
            chains=chains,
            target_hotspot_residues=target_hotspot_residues,
            lengths=[min_length, max_length],
            number_of_final_designs=number_of_designs
        )
        click.echo("Created configuration from command line arguments")
    
    # Create and run designer
    designer = BinderDesigner(settings)
    
    click.echo("Starting BindCraft NHEJ design pipeline...")
    designer.run_full_pipeline()


@cli.command()
@click.option('--design-path', required=True, help='Path to save designs')
@click.option('--binder-name', required=True, help='Name prefix for binders')
@click.option('--starting-pdb', required=True, help='Path to target PDB structure')
@click.option('--chains', default='A', help='Target chains (comma-separated)')
@click.option('--target-hotspot-residues', default='', help='Target hotspot residues')
@click.option('--min-length', default=30, help='Minimum binder length')
@click.option('--max-length', default=110, help='Maximum binder length')
@click.option('--number-of-designs', default=2, help='Number of final designs required')
@click.option('--output', help='Output JSON file path')
def create_config(
    design_path: str,
    binder_name: str,
    starting_pdb: str,
    chains: str,
    target_hotspot_residues: str,
    min_length: int,
    max_length: int,
    number_of_designs: int,
    output: Optional[str]
):
    """Create a configuration file with specified parameters."""
    
    settings = create_default_settings(
        design_path=design_path,
        binder_name=binder_name,
        starting_pdb=starting_pdb,
        chains=chains,
        target_hotspot_residues=target_hotspot_residues,
        lengths=[min_length, max_length],
        number_of_final_designs=number_of_designs
    )
    
    if not output:
        output = os.path.join(design_path, f"{binder_name}.json")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    
    settings.save(output)
    click.echo(f"Configuration saved to {output}")


@cli.command()
@click.argument('config_file')
def validate_config(config_file: str):
    """Validate a configuration file."""
    
    if not os.path.exists(config_file):
        click.echo(f"Error: Configuration file {config_file} not found", err=True)
        return
    
    try:
        settings = Settings.load(config_file)
        click.echo(f"✓ Configuration file {config_file} is valid")
        click.echo(f"  Binder name: {settings.binder_name}")
        click.echo(f"  Starting PDB: {settings.starting_pdb}")
        click.echo(f"  Target chains: {settings.chains}")
        click.echo(f"  Length range: {settings.lengths[0]}-{settings.lengths[1]}")
        click.echo(f"  Number of designs: {settings.number_of_final_designs}")
        
        # Check if starting PDB exists
        if not os.path.exists(settings.starting_pdb):
            click.echo(f"⚠ Warning: Starting PDB file not found: {settings.starting_pdb}")
        
    except Exception as e:
        click.echo(f"✗ Configuration file {config_file} is invalid: {e}", err=True)


@cli.command()
def check_environment():
    """Check if the environment is properly set up for running BindCraft NHEJ."""
    
    click.echo("Checking BindCraft NHEJ environment...")
    
    # Check Python version
    import sys
    click.echo(f"Python version: {sys.version}")
    
    # Check JAX
    try:
        import jax
        click.echo(f"✓ JAX version: {jax.__version__}")
        devices = jax.devices()
        click.echo(f"✓ JAX devices: {devices}")
    except ImportError:
        click.echo("✗ JAX not installed")
    
    # Check other key dependencies
    dependencies = [
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("dm-haiku", "haiku"),
        ("chex", "chex"),
        ("optax", "optax")
    ]
    
    for name, import_name in dependencies:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            click.echo(f"✓ {name}: {version}")
        except ImportError:
            click.echo(f"✗ {name}: not installed")


if __name__ == '__main__':
    cli()