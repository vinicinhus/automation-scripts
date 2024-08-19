from sftp_manager import SFTPManager


def main():
    # Initialize the SFTPManager with connection details
    sftp_manager = SFTPManager(
        hostname="example.com",
        port=22,
        username="your_username",
        password="your_password",
    )

    try:
        # Upload a single file
        sftp_manager.upload_file(
            local_path="local/file.txt", remote_path="remote/file.txt"
        )
        print("File uploaded successfully.")

        # Upload multiple files
        files_to_upload = {
            "local/file1.csv": "remote/file1.csv",
            "local/file2.csv": "remote/file2.csv",
        }
        sftp_manager.upload_files(files_to_upload)
        print("Multiple files uploaded successfully.")

        # Download a file
        sftp_manager.download_file(
            remote_path="remote/file.txt", local_path="local/downloaded_file.txt"
        )
        print("File downloaded successfully.")

        # List files in the remote directory
        files = sftp_manager.list_files(remote_directory="/remote")
        print("Files in remote directory:", files)

        # Rename a file on the SFTP server
        sftp_manager.rename_file(
            old_path="remote/file.txt", new_path="remote/renamed_file.txt"
        )
        print("File renamed successfully.")

        # Delete a file from the SFTP server
        sftp_manager.delete_file("remote/renamed_file.txt")
        print("File deleted successfully.")

    finally:
        # Ensure the SFTP connection is closed
        sftp_manager.disconnect()
        print("SFTP connection closed.")


if __name__ == "__main__":
    main()
