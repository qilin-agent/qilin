import os
from qilin.utils.storage.storageabc import Storage


class LocalStorage(Storage):
    """
    Local storage reads and writes files from the local file system
    """
    def __init__(self, root_path) -> None:
        super().__init__()
        self.root_path = root_path

    def save_bytes(self, path: str, data: bytes, overwrite: bool=True) -> bool:
        # Join root path and path using os.path.join
        path = os.path.join(self.root_path, path)
        # Check if the joined path exists and is a file
        if (not overwrite) and os.path.isfile(path):
            return False
        # Write data to the joined path, overwriting if necessary
        with open(path, 'wb') as f:
            f.write(data)
        return True

    def read_all_bytes(self, path: str) -> bytes:
        # Join root path and path using os.path.join
        path = os.path.join(self.root_path, path)
        # Read data from the joined path
        with open(path, 'rb') as f:
            data = f.read()
        return data
    
    def file_exists(self, path: str) -> bool:
        # Join root path and path using os.path.join
        path = os.path.join(self.root_path, path)
        # Check if the joined path exists and is a file
        return os.path.isfile(path)
    
    def delete(self, path: str) -> bool:
        # Join root path and path using os.path.join
        path = os.path.join(self.root_path, path)
        # Remove the joined path if it exists and is a file
        if os.path.isfile(path):
            os.remove(path)
            return True
        return False
