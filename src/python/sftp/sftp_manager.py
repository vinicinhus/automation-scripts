"""
Module: sftp_manager

This module provides a class for managing SFTP connections and file operations using Paramiko.

Dependencies:
- paramiko: SSH2 protocol implementation for Python.
- loguru: Logging library for Python.

Classes:
- SFTPManager: A class to manage SFTP connections and file operations.

Usage Example:
    # Initialize SFTPManager
    sftp_manager = SFTPManager(hostname='example.com', port=22, username='user', password='password')
    
    # Upload a file
    sftp_manager.upload_file(local_path='local/file.txt', remote_path='remote/file.txt')
    
    # Download a file
    sftp_manager.download_file(remote_path='remote/file.txt', local_path='local/file.txt')
    
    # Close the SFTP connection
    sftp_manager.disconnect()
"""

import socket

import paramiko
from loguru import logger


class SFTPManager:
    """
    A class to manage SFTP connections and file operations.

    Attributes:
    - hostname (str): The hostname of the SFTP server.
    - port (int): The port number of the SFTP server.
    - username (str): The username for authentication.
    - password (str): The password for authentication.
    - transport: The paramiko.Transport object for the connection.
    - sftp: The paramiko.SFTPClient object for file operations.
    """

    def __init__(self, hostname: str, port: int, username: str, password: str) -> None:
        """
        Initializes the SFTPManager with the provided credentials and establishes a connection.

        Args:
        - hostname: The hostname of the SFTP server.
        - port: The port number of the SFTP server.
        - username: The username for authentication.
        - password: The password for authentication.
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.sftp = None
        self.connect()

    def connect(self) -> None:
        """
        Establishes a connection to the SFTP server.

        Raises:
        - paramiko.AuthenticationException: If authentication fails.
        - paramiko.SSHException: If an SSH-related error occurs.
        - socket.error: If a socket error occurs.
        - Exception: For any other unexpected errors.
        """
        try:
            self.transport = paramiko.Transport((self.hostname, self.port))
            self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.AuthenticationException as auth_error:
            logger.error(f"Authentication failed: {auth_error}")
            raise
        except paramiko.SSHException as ssh_error:
            logger.error(f"SSH error occurred: {ssh_error}")
            raise
        except socket.error as socket_error:
            logger.error(f"Socket error occurred: {socket_error}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while trying to connect to the SFTP server: {e}"
            )
            raise

    def disconnect(self) -> None:
        """
        Closes the SFTP connection.

        Raises:
        - AttributeError: If there's an attribute error.
        - IOError: If an IO error occurs.
        - paramiko.SSHException: If an SSH-related error occurs.
        - Exception: For any other unexpected errors.
        """
        try:
            if self.sftp:
                self.sftp.close()
            if self.transport:
                self.transport.close()
        except AttributeError as attr_error:
            logger.error(f"Attribute error occurred: {attr_error}")
            raise
        except IOError as io_error:
            logger.error(f"IO error occured: {io_error}")
            raise
        except paramiko.SSHException as ssh_error:
            logger.error(f"SSH error occurred: {ssh_error}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while trying to disconnect from the SFTP server: {e}"
            )

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Uploads a file from the local system to the SFTP server.

        Args:
        - local_path: The local path of the file to upload.
        - remote_path: The remote path where the file will be uploaded on the server.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        try:
            self.sftp.put(local_path, remote_path)
        except paramiko.SSHException as ssh_error:
            logger.error(
                f"SSH error occurred while uploading file '{local_path}' to '{remote_path}': {ssh_error}"
            )
            raise
        except paramiko.SFTPError as sftp_error:
            logger.error(
                f"SFTP error occurred while uploading file '{local_path}' to '{remote_path}': {sftp_error}"
            )
            raise
        except OSError as os_error:
            logger.error(
                f"OS error occurred while uploading file '{local_path}' to '{remote_path}': {os_error}"
            )
            raise

    def upload_files(self, file_mapping: dict) -> None:
        """
        Uploads multiple files from the local system to the SFTP server.

        Args:
        - file_mapping: A dictionary where keys are local paths and values are remote paths.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        for local_path, remote_path in file_mapping.items():
            try:
                self.sftp.put(local_path, remote_path)
            except paramiko.SSHException as ssh_error:
                logger.error(
                    f"SSH error occurred while uploading file '{local_path}' to '{remote_path}': {ssh_error}"
                )
                raise
            except paramiko.SFTPError as sftp_error:
                logger.error(
                    f"SFTP error occurred while uploading file '{local_path}' to '{remote_path}': {sftp_error}"
                )
                raise
            except OSError as os_error:
                logger.error(
                    f"OS error occurred while uploading file '{local_path}' to '{remote_path}': {os_error}"
                )
                raise
        logger.info("All the .csv files has been uploaded to the SFTP directory")

    def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Downloads a file from the SFTP server to the local system.

        Args:
        - remote_path: The remote path of the file on the server.
        - local_path: The local path where the file will be downloaded.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        try:
            self.sftp.get(remote_path, local_path)
        except paramiko.SSHException as ssh_error:
            logger.error(
                f"SSH error occurred while downloading file '{remote_path}' to '{local_path}': {ssh_error}"
            )
            raise
        except paramiko.SFTPError as sftp_error:
            logger.error(
                f"SFTP error occurred while downloading file '{remote_path}' to '{local_path}': {sftp_error}"
            )
            raise
        except OSError as os_error:
            logger.error(
                f"OS error occurred while downloading file '{remote_path}' to '{local_path}': {os_error}"
            )
            raise

    def copy_file(self, source_path: str, destination_path: str) -> None:
        """
        Copies a file from one location to another on the SFTP server.

        Args:
        - source_path: The source path of the file.
        - destination_path: The destination path where the file will be copied.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        try:
            self.sftp.put(source_path, destination_path)
        except paramiko.SSHException as ssh_error:
            logger.error(
                f"SSH error occurred while copying file '{source_path}' to '{destination_path}': {ssh_error}"
            )
            raise
        except paramiko.SFTPError as sftp_error:
            logger.error(
                f"SFTP error occurred while copying file '{source_path}' to '{destination_path}': {sftp_error}"
            )
            raise
        except OSError as os_error:
            logger.error(
                f"OS error occurred while copying file '{source_path}' to '{destination_path}': {os_error}"
            )
            raise

    def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Renames a file on the SFTP server.

        Args:
        - old_path: The current path of the file.
        - new_path: The new path to rename the file.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        try:
            self.sftp.rename(old_path, new_path)
        except paramiko.SSHException as ssh_error:
            logger.error(
                f"SSH error occurred while renaming file '{old_path}' to '{new_path}': {ssh_error}"
            )
            raise
        except paramiko.SFTPError as sftp_error:
            logger.error(
                f"SFTP error occurred while renaming file '{old_path}' to '{new_path}': {sftp_error}"
            )
            raise
        except OSError as os_error:
            logger.error(
                f"OS error occurred while renaming file '{old_path}' to '{new_path}': {os_error}"
            )
            raise

    def list_files(self, remote_directory: str = ".") -> list[str]:
        """
        Lists files in a remote directory on the SFTP server.

        Args:
        - remote_directory: The remote directory path. Defaults to the current directory.

        Returns:
        - List[str]: A list of filenames in the remote directory.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        try:
            files = self.sftp.listdir_attr(remote_directory)
            return [
                file.filename for file in files if not file.filename.startswith(".")
            ]
        except paramiko.SSHException as ssh_error:
            logger.error(
                f"SSH error occurred while listing files in directory '{remote_directory}': {ssh_error}"
            )
            raise
        except paramiko.SFTPError as sftp_error:
            logger.error(
                f"SFTP error occurred while listing files in directory '{remote_directory}': {sftp_error}"
            )
            raise
        except OSError as os_error:
            logger.error(
                f"OS error occurred while listing files in directory '{remote_directory}': {os_error}"
            )
            raise

    def delete_file(self, file_path: str) -> None:
        """
        Deletes a file from the SFTP server.

        Args:
        - file_path: The path of the file to delete.

        Raises:
        - paramiko.SSHException: If an SSH-related error occurs.
        - paramiko.SFTPError: If an SFTP-related error occurs.
        - OSError: If an OS-related error occurs.
        """
        try:
            self.sftp.remove(file_path)
        except paramiko.SSHException as ssh_error:
            logger.error(
                f"SSH error occurred while deleting file '{file_path}': {ssh_error}"
            )
            raise
        except paramiko.SFTPError as sftp_error:
            logger.error(
                f"SFTP error occurred while deleting file '{file_path}': {sftp_error}"
            )
            raise
        except OSError as os_error:
            logger.error(
                f"OS error occurred while deleting file '{file_path}': {os_error}"
            )
            raise
