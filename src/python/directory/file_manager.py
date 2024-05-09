"""
Module: file_manager.py

This module provides a FileManager class for managing files and folders within a directory.

Dependencies:
    - datetime: Provides classes for manipulating dates and times.
    - pathlib: Provides an object-oriented interface for working with file system paths.
    - typing: Provides support for type hints.
    - time: Provides time-related functions for waiting until a file is present.

Usage Example:
    >>> from file_manager import FileManager

    >>> # Initialize FileManager with the current directory as the base path
    >>> file_manager = FileManager()

    >>> # Rename a file
    >>> file_manager.rename_file("old_file.txt", "new_file.txt")

    >>> # Move a file to a different location
    >>> file_manager.move_file("file.txt", "destination_folder")

    >>> # Rename multiple files using a mapping dictionary
    >>> path_mapping = {"old_file1.txt": "new_file1.txt", "old_file2.txt": "new_file2.txt"}
    >>> file_manager.rename_files(path_mapping)

    >>> # Move multiple files to different locations using a mapping dictionary
    >>> path_mapping = {"file1.txt": "destination_folder1", "file2.txt": "destination_folder2"}
    >>> file_manager.move_files(path_mapping)

    >>> # Exclude (delete) a file
    >>> file_manager.exclude_file("file_to_delete.txt")

    >>> # Exclude (delete) all files in a folder
    >>> file_manager.exclude_files_in_folder("folder_to_clear")

    >>> # Create a new folder if it does not already exist
    >>> created_folder_path = file_manager.create_folder("new_folder")
    
    >>> # Wait until a file with the specified extension is present in a folder
    >>> file_manager.wait_until_file_is_present("folder_path", "file_extension", timeout=60)
"""

from datetime import datetime
from pathlib import Path
from typing import Dict
import time


class FileManager:
    def __init__(self) -> None:
        """
        Initialize FileManager with the current directory as the base path.
        """
        self.base_path: Path = Path.cwd()

    def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file.

        Args:
            old_path: The name of the file to be renamed.
            new_path: The new name for the file.
        """
        file_path: Path = self.base_path / old_path
        file_path.rename(self.base_path / new_path)

    def move_file(self, file_path: str, destination: str) -> None:
        """
        Move a file to a different location.

        Args:
            file_path: The name of the file to be moved.
            destination: The destination folder path where the file will be moved.
        """
        file_path: Path = self.base_path / file_path
        destination_path: Path = self.base_path / destination
        file_path.rename(destination_path / file_path)

    def rename_files(self, path_mapping: Dict[str, str]) -> None:
        """
        Rename multiple files using a mapping dictionary.

        Args:
            path_mapping: A dictionary where keys are the old file names and values are the new file names.
        """
        for old_path, new_path in path_mapping.items():
            self.rename_file(old_path, new_path)

    def move_files(self, path_mapping: Dict[str, str]) -> None:
        """
        Move multiple files to different locations using a mapping dictionary.

        Args:
            path_mapping: A dictionary where keys are the file names and values are the destination folder paths.
        """
        for file_path, destination in path_mapping.items():
            self.move_file(file_path, destination)

    def exclude_file(self, file_path: str) -> None:
        """
        Exclude (delete) a file.

        Args:
            file_path: The name of the file to be excluded (deleted).
        """
        file_path: Path = self.base_path / file_path
        file_path.unlink()

    def exclude_files_in_folder(self, folder_path: str) -> None:
        """
        Exclude (delete) all files in a folder.

        Args:
            folder_path: The name of the folder containing files to be excluded (deleted).
        """
        folder_path: Path = self.base_path / folder_path
        for file_path in folder_path.iterdir():
            file_path.unlink()

    def create_folder(self, folder_path: str) -> Path:
        """
        Create a new folder if it does not already exist.

        Args:
            folder_path: The name of the new folder to be created.
                         If the string contains '{time:YYYY-MM-DD}', it will be replaced
                         with the current date in the specified format.
                         
        Returns:
            Path: The path of the created folder.
        """
        if '{time:YYYY-MM-DD}' in folder_path:
            current_date = datetime.now().strftime("%Y-%m-%d")
            folder_path = folder_path.replace('{time:YYYY-MM-DD}', current_date)

        folder_path: Path = self.base_path / folder_path
        if not folder_path.exists():
            folder_path.mkdir()
        return folder_path
    
    def wait_until_file_is_present(self, folder_path: str, file_extension: str, timeout: int = 60):
        """
        Wait until a file with the specified extension is present in a folder.

        Args:
            folder_path: The path of the folder to search for the file.
            file_extension: The extension of the file to wait for.
            timeout: The maximum time (in seconds) to wait for the file before raising a TimeoutError.
        """
        start_time = time.time()
        folder_path: Path = self.base_path / folder_path
        
        while True:
            files = [f for f in folder_path.glob(f"*.{file_extension.lower()}")]
        
            if files:
                break
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                raise TimeoutError(f"Timeout: No {file_extension.upper()} file found within {timeout} seconds")
            
            time.sleep(1)
            