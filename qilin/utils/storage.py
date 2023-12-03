from abc import ABC, abstractmethod
import os


class Storage(ABC):
    """
    Abstract class for storage
    """
    @abstractmethod
    def save_bytes(self, path: str, data: bytes, overwrite: bool=True) -> bool:
        pass

    def save_string(self, path: str, data: str, overwrite: bool=True, encoding: str='utf-8') -> bool:
        return self.save_bytes(path, data.encode(encoding), overwrite)

    @abstractmethod
    def read_all_bytes(self, path: str) -> bytes:
        pass

    def read_all_string(self, path: str, encoding: str='utf-8') -> str:
        return self.read_all_bytes(path).decode(encoding)
    
    @abstractmethod
    def file_exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        pass


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


class AzureBlobStorage(Storage):
    """
    Azure Blob Storage reads and writes files from Azure Blob Storage
    """
    def __init__(self, container_url: str, sas_token: str) -> None:
        super().__init__()
        self.container_url = container_url
        from azure.storage.blob import ContainerClient
        self.container_client = ContainerClient.from_container_url(container_url, credential=sas_token)

    def save_bytes(self, path: str, data: bytes, overwrite: bool=True) -> bool:
        # Check if the path exists and is a file
        if (not overwrite) and self.file_exists(path):
            return False
        # Upload data to the path, overwriting if necessary
        self.container_client.upload_blob(name=path, data=data, overwrite=overwrite)
        return True
    
    def read_all_bytes(self, path: str) -> bytes:
        # Download data from the path
        data = self.container_client.download_blob(path).readall()
        return data
    
    def file_exists(self, path: str) -> bool:
        # Check if the path exists and is a file
        return self.container_client.get_blob_client(path).exists()
    
    def delete(self, path: str) -> bool:
        # Delete the path if it exists and is a file
        if self.file_exists(path):
            self.container_client.delete_blob(path)
            return True
        return False

