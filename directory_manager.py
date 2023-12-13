import os


class DirectoryManager:
    @staticmethod
    def create_directory(base_path, directory_name):
        """
        Create a directory if it doesn't exist and return the full path.

        Args:
            base_path (str): The base path where the directory should be created.
            directory_name (str): The name of the directory to be created.

        Returns:
            str: The full path of the created directory.
        """
        full_path = os.path.join(base_path, directory_name)

        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Directory '{directory_name}' created at '{full_path}'")

        return full_path
