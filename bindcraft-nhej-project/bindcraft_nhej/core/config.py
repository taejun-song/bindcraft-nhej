"""Configuration management for BindCraft NHEJ."""

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class Settings:
    """Main settings for binder design."""
    
    design_path: str
    binder_name: str
    starting_pdb: str
    chains: str
    target_hotspot_residues: str
    lengths: List[int]
    number_of_final_designs: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        """Create Settings from dictionary."""
        return cls(
            design_path=data["design_path"],
            binder_name=data["binder_name"],
            starting_pdb=data["starting_pdb"],
            chains=data["chains"],
            target_hotspot_residues=data["target_hotspot_residues"],
            lengths=data["lengths"],
            number_of_final_designs=data["number_of_final_designs"]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Settings to dictionary."""
        return {
            "design_path": self.design_path,
            "binder_name": self.binder_name,
            "starting_pdb": self.starting_pdb,
            "chains": self.chains,
            "target_hotspot_residues": self.target_hotspot_residues,
            "lengths": self.lengths,
            "number_of_final_designs": self.number_of_final_designs
        }
    
    def save(self, filepath: str) -> None:
        """Save settings to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    @classmethod
    def load(cls, filepath: str) -> 'Settings':
        """Load settings from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class AdvancedSettings:
    """Advanced settings for design protocols."""
    
    # Design protocol settings
    design_protocol: str = "Default"
    interface_protocol: str = "AlphaFold2"
    template_protocol: str = "Default"
    
    # AA restrictions
    omit_AAs: str = 'C'
    force_reject_AA: bool = False
    
    # Model settings
    use_multimer_design: bool = True
    design_algorithm: str = '4stage'
    sample_models: bool = True
    
    # Template settings
    rm_template_seq_design: bool = False
    rm_template_seq_predict: bool = False
    rm_template_sc_design: bool = False
    rm_template_sc_predict: bool = False
    
    # Iteration settings
    soft_iterations: int = 75
    temporary_iterations: int = 45
    hard_iterations: int = 5
    greedy_iterations: int = 15
    greedy_percentage: int = 1
    
    # Weights
    weights_plddt: float = 0.1
    weights_pae_intra: float = 0.4
    weights_pae_inter: float = 0.1
    weights_con_intra: float = 1.0
    weights_con_inter: float = 1.0
    weights_helicity: float = -0.3
    weights_iptm: float = 0.05
    weights_rg: float = 0.3
    weights_termini_loss: float = 0.1
    
    # Contact settings
    intra_contact_distance: float = 14.0
    inter_contact_distance: float = 20.0
    intra_contact_number: int = 2
    inter_contact_number: int = 2
    
    # Loss function settings
    random_helicity: bool = False
    use_i_ptm_loss: bool = True
    use_rg_loss: bool = True
    use_termini_distance_loss: bool = False
    
    # MPNN settings
    enable_mpnn: bool = True
    mpnn_fix_interface: bool = True
    num_seqs: int = 20
    max_mpnn_sequences: int = 2
    sampling_temp: float = 0.1
    backbone_noise: float = 0.0
    model_path: str = 'v_48_020'
    mpnn_weights: str = 'soluble'
    save_mpnn_fasta: bool = False
    
    # Recycling settings
    num_recycles_design: int = 1
    num_recycles_validation: int = 3
    
    # Beta optimization
    optimise_beta: bool = True
    optimise_beta_extra_soft: int = 0
    optimise_beta_extra_temp: int = 0
    optimise_beta_recycles_design: int = 3
    optimise_beta_recycles_valid: int = 3
    
    # File management
    save_design_animations: bool = True
    save_design_trajectory_plots: bool = True
    remove_unrelaxed_trajectory: bool = True
    remove_unrelaxed_complex: bool = True
    remove_binder_monomer: bool = True
    zip_animations: bool = True
    zip_plots: bool = True
    save_trajectory_pickle: bool = False
    
    # Trajectory limits
    max_trajectories: bool = False
    enable_rejection_check: bool = True
    acceptance_rate: float = 0.01
    start_monitoring: int = 600
    
    # Paths (to be set later)
    af_params_dir: str = ""
    dssp_path: str = ""
    dalphaball_path: str = ""


def create_default_settings(
    design_path: str,
    binder_name: str, 
    starting_pdb: str,
    chains: str = "A",
    target_hotspot_residues: str = "",
    lengths: List[int] = [30, 110],
    number_of_final_designs: int = 2
) -> Settings:
    """Create default settings configuration."""
    return Settings(
        design_path=design_path,
        binder_name=binder_name,
        starting_pdb=starting_pdb,
        chains=chains,
        target_hotspot_residues=target_hotspot_residues,
        lengths=lengths,
        number_of_final_designs=number_of_final_designs
    )


def update_settings_timestamp(settings_path: str) -> str:
    """Update settings with current timestamp."""
    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Binder design settings updated at: {currenttime}")
    print(f"Settings file: {settings_path}")
    return currenttime