from datetime import datetime
from pathlib import Path
from typing import Dict


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

    def create_folder(self, folder_path: str) -> str:
        """
        Create a new folder if it does not already exist.

        Args:
            folder_path: The name of the new folder to be created.
                         If the string contains '{time:YYYY-MM-DD}', it will be replaced
                         with the current date in the specified format.
                         
        Returns:
            str: The path of the created folder.
        """
        if '{time:YYYY-MM-DD}' in folder_path:
            current_date = datetime.now().strftime("%Y-%m-%d")
            folder_path = folder_path.replace('{time:YYYY-MM-DD}', current_date)

        folder_path: Path = self.base_path / folder_path
        if not folder_path.exists():
            folder_path.mkdir()
        return str(folder_path)
