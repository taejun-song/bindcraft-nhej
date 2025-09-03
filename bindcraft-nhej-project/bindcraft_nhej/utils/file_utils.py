"""File utility functions extracted from the notebook."""

import os
import shutil
from typing import Optional


def delete_directory(directory_path: str) -> None:
    """
    Delete specified directory. Removes all files and subdirectories if directory is not empty.
    
    Args:
        directory_path: Path to the directory to delete
    """
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Directory {directory_path} has been deleted successfully.")
        except Exception as e:
            print(f"Failed to delete directory {directory_path}: {e}")
    else:
        print(f"Directory {directory_path} does not exist.")


def ensure_directory(directory_path: str) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to the directory to create
    """
    os.makedirs(directory_path, exist_ok=True)


def copy_file_safe(source: str, destination: str) -> bool:
    """
    Safely copy a file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if copy was successful, False otherwise
    """
    try:
        shutil.copy(source, destination)
        return True
    except Exception as e:
        print(f"Failed to copy {source} to {destination}: {e}")
        return False


def get_file_extension(filepath: str) -> str:
    """Get file extension from filepath."""
    return os.path.splitext(filepath)[1].lower()


def is_pdb_file(filepath: str) -> bool:
    """Check if file is a PDB file."""
    return get_file_extension(filepath) == '.pdb'


def find_files_with_pattern(directory: str, pattern: str) -> list:
    """
    Find files in directory matching a pattern.
    
    Args:
        directory: Directory to search
        pattern: Filename pattern to match
        
    Returns:
        List of matching file paths
    """
    import glob
    return glob.glob(os.path.join(directory, pattern))


def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return os.path.exists(filepath) and os.path.isfile(filepath)


def check_directory_exists(directory_path: str) -> bool:
    """Check if a directory exists."""
    return os.path.exists(directory_path) and os.path.isdir(directory_path)


def get_basename_without_extension(filepath: str) -> str:
    """Get basename of file without extension."""
    return os.path.splitext(os.path.basename(filepath))[0]


def create_backup(filepath: str, backup_suffix: str = ".backup") -> Optional[str]:
    """
    Create a backup of a file.
    
    Args:
        filepath: File to backup
        backup_suffix: Suffix for backup file
        
    Returns:
        Path to backup file if successful, None otherwise
    """
    if not check_file_exists(filepath):
        return None
        
    backup_path = filepath + backup_suffix
    if copy_file_safe(filepath, backup_path):
        return backup_path
    return None