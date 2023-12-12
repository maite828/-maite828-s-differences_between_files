import os


class DirectoryManager:
    @staticmethod
    def create_directory(base_path, directory_name):
        full_path = os.path.join(base_path, directory_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            print(f"Directory '{directory_name}' created at '{full_path}'")
        return full_path
