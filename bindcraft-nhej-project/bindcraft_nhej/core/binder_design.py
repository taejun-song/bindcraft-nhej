"""Main binder design class and workflow."""

import os
import time
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any

from ..core.config import Settings, AdvancedSettings
from ..utils.file_utils import ensure_directory, check_file_exists
from ..utils.environment import check_jax_gpu, validate_required_tools


class BinderDesigner:
    """Main class for BindCraft NHEJ binder design workflow."""
    
    def __init__(
        self, 
        settings: Settings,
        advanced_settings: Optional[AdvancedSettings] = None,
        filters_path: Optional[str] = None
    ):
        """
        Initialize BinderDesigner.
        
        Args:
            settings: Main design settings
            advanced_settings: Advanced protocol settings
            filters_path: Path to filters configuration
        """
        self.settings = settings
        self.advanced_settings = advanced_settings or AdvancedSettings()
        self.filters_path = filters_path
        
        # Initialize paths
        self.design_paths = {}
        self.csv_paths = {}
        
        # Counters
        self.trajectory_n = 1
        self.accepted_designs = 0
        self.script_start_time = None
        
    def validate_environment(self) -> bool:
        """Validate that the environment is properly set up."""
        print("Validating environment...")
        
        # Check JAX GPU availability
        check_jax_gpu()
        
        # Check required files
        if not check_file_exists(self.settings.starting_pdb):
            print(f"Error: Starting PDB file not found: {self.settings.starting_pdb}")
            return False
            
        # Validate required tools if paths are set
        required_tools = []
        if self.advanced_settings.dssp_path:
            required_tools.append(self.advanced_settings.dssp_path)
        if self.advanced_settings.dalphaball_path:
            required_tools.append(self.advanced_settings.dalphaball_path)
            
        if required_tools:
            return validate_required_tools(required_tools)
            
        return True
    
    def setup_directories(self) -> None:
        """Set up directory structure for design output."""
        base_path = self.settings.design_path
        
        self.design_paths = {
            "base": base_path,
            "Trajectory": os.path.join(base_path, "Trajectory"),
            "Trajectory/Relaxed": os.path.join(base_path, "Trajectory", "Relaxed"), 
            "Trajectory/LowConfidence": os.path.join(base_path, "Trajectory", "LowConfidence"),
            "Trajectory/Clashing": os.path.join(base_path, "Trajectory", "Clashing"),
            "Trajectory/Animation": os.path.join(base_path, "Trajectory", "Animation"),
            "Trajectory/Plots": os.path.join(base_path, "Trajectory", "Plots"),
            "MPNN": os.path.join(base_path, "MPNN"),
            "MPNN/Relaxed": os.path.join(base_path, "MPNN", "Relaxed"),
            "MPNN/Binder": os.path.join(base_path, "MPNN", "Binder"),
            "Accepted": os.path.join(base_path, "Accepted"),
            "Accepted/Ranked": os.path.join(base_path, "Accepted", "Ranked"),
            "Accepted/Animation": os.path.join(base_path, "Accepted", "Animation"),
            "Accepted/Plots": os.path.join(base_path, "Accepted", "Plots"),
            "Rejected": os.path.join(base_path, "Rejected")
        }
        
        # Create all directories
        for path in self.design_paths.values():
            ensure_directory(path)
            
        print(f"Created directory structure in {base_path}")
    
    def setup_dataframes(self) -> None:
        """Set up CSV files for tracking design progress."""
        base_path = self.settings.design_path
        
        self.csv_paths = {
            "trajectory": os.path.join(base_path, 'trajectory_stats.csv'),
            "mpnn": os.path.join(base_path, 'mpnn_design_stats.csv'),
            "final": os.path.join(base_path, 'final_design_stats.csv'),
            "failure": os.path.join(base_path, 'failure_stats.csv')
        }
        
        # Initialize CSV files with headers (would need actual column definitions)
        print("CSV tracking files initialized")
    
    def generate_design_name(self, length: int, seed: int) -> str:
        """Generate a unique design name."""
        return f"{self.settings.binder_name}_l{length}_s{seed}"
    
    def check_trajectory_exists(self, design_name: str) -> bool:
        """Check if a trajectory with the same name already exists."""
        trajectory_dirs = ["Trajectory", "Trajectory/Relaxed", "Trajectory/LowConfidence", "Trajectory/Clashing"]
        return any(
            os.path.exists(os.path.join(self.design_paths[trajectory_dir], design_name + ".pdb")) 
            for trajectory_dir in trajectory_dirs
        )
    
    def run_binder_hallucination(self, design_name: str, length: int, seed: int, helicity_value: float) -> Dict[str, Any]:
        """
        Run the binder hallucination process.
        
        This is a placeholder for the actual BindCraft hallucination function.
        """
        print(f"Running binder hallucination for {design_name}")
        print(f"Length: {length}, Seed: {seed}, Helicity: {helicity_value}")
        
        # Placeholder trajectory result
        trajectory_result = {
            "design_name": design_name,
            "success": True,
            "metrics": {
                "plddt": 85.0,
                "ptm": 0.8,
                "i_ptm": 0.75,
                "pae": 5.0,
                "i_pae": 4.5
            },
            "sequence": "PLACEHOLDER_SEQUENCE",
            "terminate": ""
        }
        
        return trajectory_result
    
    def run_design_loop(self) -> None:
        """Run the main design loop."""
        print("Starting BindCraft NHEJ design loop...")
        self.script_start_time = time.time()
        
        while self.accepted_designs < self.settings.number_of_final_designs:
            # Generate random parameters for this trajectory
            import numpy as np
            seed = int(np.random.randint(0, high=999999, size=1, dtype=int)[0])
            
            # Sample binder design length randomly from defined distribution
            samples = np.arange(min(self.settings.lengths), max(self.settings.lengths) + 1)
            length = np.random.choice(samples)
            
            # Load helicity value (placeholder)
            helicity_value = -0.3  # Default from advanced settings
            
            design_name = self.generate_design_name(length, seed)
            
            # Check if trajectory already exists
            if self.check_trajectory_exists(design_name):
                print(f"Trajectory {design_name} already exists, skipping...")
                continue
                
            print(f"Starting trajectory: {design_name}")
            trajectory_start_time = time.time()
            
            # Run binder hallucination (placeholder)
            trajectory_result = self.run_binder_hallucination(design_name, length, seed, helicity_value)
            
            if trajectory_result["success"]:
                # Process successful trajectory
                trajectory_time = time.time() - trajectory_start_time
                trajectory_time_text = f"{'%d hours, %d minutes, %d seconds' % (int(trajectory_time // 3600), int((trajectory_time % 3600) // 60), int(trajectory_time % 60))}"
                print(f"Trajectory {design_name} completed in: {trajectory_time_text}")
                
                # Here would go MPNN processing, filtering, etc.
                # For now, just increment accepted designs as placeholder
                self.accepted_designs += 1
                
            self.trajectory_n += 1
            
            # Safety check to prevent infinite loops
            if self.trajectory_n > 1000:
                print("Maximum trajectory limit reached, stopping...")
                break
    
    def run_full_pipeline(self) -> None:
        """Run the complete binder design pipeline."""
        print("="*50)
        print("BindCraft NHEJ Binder Design Pipeline")
        print("="*50)
        
        # Validate environment
        if not self.validate_environment():
            print("Environment validation failed. Exiting.")
            return
            
        # Setup directories and tracking
        self.setup_directories()
        self.setup_dataframes()
        
        # Save current settings
        settings_file = os.path.join(self.settings.design_path, f"{self.settings.binder_name}.json")
        self.settings.save(settings_file)
        print(f"Settings saved to: {settings_file}")
        
        # Run the design loop
        self.run_design_loop()
        
        # Final summary
        elapsed_time = time.time() - self.script_start_time
        elapsed_text = f"{'%d hours, %d minutes, %d seconds' % (int(elapsed_time // 3600), int((elapsed_time % 3600) // 60), int(elapsed_time % 60))}"
        
        print("="*50)
        print("Design Pipeline Complete")
        print(f"Total trajectories: {self.trajectory_n}")
        print(f"Accepted designs: {self.accepted_designs}")
        print(f"Total time: {elapsed_text}")
        print("="*50)
    
    @classmethod
    def create_default(
        cls,
        design_path: str,
        binder_name: str,
        starting_pdb: str,
        **kwargs
    ) -> 'BinderDesigner':
        """Create a BinderDesigner with default settings."""
        from ..core.config import create_default_settings
        
        settings = create_default_settings(
            design_path=design_path,
            binder_name=binder_name,
            starting_pdb=starting_pdb,
            **kwargs
        )
        
        return cls(settings)