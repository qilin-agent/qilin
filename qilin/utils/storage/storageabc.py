from abc import ABC, abstractmethod


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
