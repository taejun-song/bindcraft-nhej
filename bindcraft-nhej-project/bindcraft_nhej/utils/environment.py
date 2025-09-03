"""Environment setup and validation utilities."""

import os
import sys
import contextlib
import io
from typing import List, Tuple


def check_jax_gpu() -> None:
    """Check if JAX-capable GPU is available."""
    try:
        import jax
        devices = jax.devices()
        print("Available devices:", devices)
        
        # Check for GPU
        gpu_devices = [d for d in devices if 'gpu' in str(d).lower() or 'cuda' in str(d).lower()]
        if not gpu_devices:
            print("Warning: No GPU devices found. JAX will run on CPU.")
        else:
            for device in gpu_devices:
                print(f"Found GPU device: {device}")
                
    except ImportError:
        print("JAX not installed or not available")
        sys.exit(1)


def setup_jax_environment() -> None:
    """Set up JAX environment with specific versions."""
    print("Setting up JAX environment...")
    
    # These would be handled by package management instead
    required_packages = [
        "jax==0.4.30",
        "jaxlib==0.4.30", 
        "dm-haiku==0.0.12",
        "chex==0.1.86",
        "optax==0.1.7"
    ]
    
    print(f"Required packages: {', '.join(required_packages)}")
    print("Note: Use 'uv add' to install these dependencies")


def check_python_environment() -> Tuple[str, str]:
    """Check Python environment and JAX version."""
    python_path = sys.executable
    
    try:
        import jax
        jax_version = jax.__version__
    except ImportError:
        jax_version = "Not installed"
    
    print(f"Python: {python_path}")
    print(f"JAX version: {jax_version}")
    
    return python_path, jax_version


def setup_pyrosetta_silent() -> None:
    """Set up PyRosetta with silent output."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import pyrosettacolabsetup
            pyrosettacolabsetup.install_pyrosetta(
                serialization=True, 
                cache_wheel_on_google_drive=False
            )
        print("PyRosetta setup completed silently")
    except ImportError:
        print("PyRosetta setup tools not available")


def validate_required_tools(tools: List[str]) -> bool:
    """
    Validate that required external tools are available.
    
    Args:
        tools: List of tool names/paths to validate
        
    Returns:
        True if all tools are available
    """
    missing_tools = []
    
    for tool in tools:
        if not (os.path.exists(tool) and os.access(tool, os.X_OK)):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"Missing required tools: {', '.join(missing_tools)}")
        return False
    
    print("All required tools are available")
    return True


def setup_bindcraft_paths(bindcraft_folder: str = "bindcraft") -> dict:
    """
    Set up BindCraft-specific paths.
    
    Args:
        bindcraft_folder: Base folder for BindCraft
        
    Returns:
        Dictionary of important paths
    """
    paths = {
        "bindcraft": bindcraft_folder,
        "params": os.path.join(bindcraft_folder, "params"),
        "functions": os.path.join(bindcraft_folder, "functions"),
        "dssp": os.path.join(bindcraft_folder, "functions", "dssp"),
        "dalphaball": os.path.join(bindcraft_folder, "functions", "DAlphaBall.gcc")
    }
    
    return paths