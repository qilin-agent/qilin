from abc import ABC, abstractmethod
from typing import AsyncIterable
from typing import TypeVar
from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)


class Storage(ABC):
    """
    Abstract class for storage
    """
    @abstractmethod
    async def save_bytes(self, path: str, data: bytes, overwrite: bool=True) -> bool:
        pass

    @abstractmethod
    async def read_all_bytes(self, path: str) -> bytes:
        pass
    
    @abstractmethod
    async def file_exists(self, path: str) -> bool:
        pass
    
    @abstractmethod
    async def delete_file(self, path: str) -> bool:
        pass

    async def save_str(self, path: str, data: str, overwrite: bool=True, encoding: str='utf-8') -> bool:
        return await self.save_bytes(path, data.encode(encoding), overwrite=overwrite)
    
    async def read_all_str(self, path: str, encoding: str='utf-8') -> str:
        return (await self.read_all_bytes(path)).decode(encoding)
    
    async def read_json(self, path: str, obj_type: type[T], encoding: str='utf-8') -> T:
        json_str = await self.read_all_str(path, encoding=encoding)
        return obj_type.model_validate_json(json_str)
    
    async def save_json(self, path: str, data: T, overwrite: bool=True, encoding: str='utf-8') -> bool:
        json_str = data.model_dump_json()
        return await self.save_str(path, json_str, overwrite=overwrite, encoding=encoding)
    
    @abstractmethod
    async def get_row(self, partition_key: str, row_key: str) -> dict:
        pass
    
    @abstractmethod
    async def query_rows(self, partition_key: str, row_start: str=None, row_end: str=None, top: int=None) -> AsyncIterable[dict]:
        pass

    @abstractmethod
    async def upsert_row(self, entity: dict) -> None:
        pass

    @abstractmethod
    async def delete_row(self, entity: dict) -> None:
        pass
