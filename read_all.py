import os


def read_files_content(root_folder):
    for subdir, dirs, files in os.walk(root_folder):
        # Skip __pycache__ directories and any subdirectories within them
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')

        if '.coverage' in dirs:
            dirs.remove('coverage')

        if '.pytest_cache' in dirs:
            dirs.remove('.pytest_cache')

        for file in files:
            try:
                file_path = os.path.join(subdir, file)
                print(f"Reading file: {file_path}\n----\n")

                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                    print(contents)

                print("\n----\n\n")  # Separator between file contents
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")


if __name__ == "__main__":
    root_folder_path = input("Enter the root folder path: ").strip()
    read_files_content(root_folder_path)
