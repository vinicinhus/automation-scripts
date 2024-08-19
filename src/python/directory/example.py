from file_manager import FileManager


def main():
    # Initialize FileManager with the current directory as the base path
    file_manager = FileManager()

    # Example 1: Rename a file
    file_manager.rename_file("old_file.txt", "new_file.txt")

    # Example 2: Move a file to a different location
    file_manager.move_file("file.txt", "destination_folder")

    # Example 3: Rename multiple files using a mapping dictionary
    path_mapping = {"old_file1.txt": "new_file1.txt", "old_file2.txt": "new_file2.txt"}
    file_manager.rename_files(path_mapping)

    # Example 4: Move multiple files to different locations using a mapping dictionary
    path_mapping = {
        "file1.txt": "destination_folder1",
        "file2.txt": "destination_folder2",
    }
    file_manager.move_files(path_mapping)

    # Example 5: Move all files from one folder to a destination folder
    file_manager.move_all_files("source_folder", "destination_folder")

    # Example 6: Exclude (delete) a file
    file_manager.exclude_file("file_to_delete.txt")

    # Example 7: Exclude (delete) all files in a folder
    file_manager.exclude_all_files("folder_to_clear")

    # Example 8: Clear all files from a directory tree
    file_manager.clear_directory_tree("directory_to_clear")

    # Example 9: Create a new folder if it does not already exist
    created_folder_path = file_manager.create_folder("new_folder")
    print(f"Created folder: {created_folder_path}")

    # Example 10: Wait until a file with the specified extension is present in a folder
    try:
        file_manager.wait_until_file_is_present("folder_path", ".txt", timeout=60)
        print("A .txt file is present in the folder.")
    except TimeoutError as e:
        print(e)

    # Example 11: Check if a file with the extension .txt exists in a folder
    has_txt_in_folder = file_manager.has_file_with_extension("/path/to/folder", ".txt")
    if has_txt_in_folder:
        print("A .txt file exists in the folder.")
    else:
        print("No .txt file found in the folder.")


if __name__ == "__main__":
    main()
