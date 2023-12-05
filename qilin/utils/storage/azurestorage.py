from qilin.utils.storage.storageabc import Storage
from typing import AsyncIterable
import os


class AzureStorage(Storage):
    """
    Azure Blob Storage reads and writes files from Azure Blob Storage
    """
    def __init__(
            self,
            container_url: str=None,
            container_sas: str=None,
            table_url: str=None,
            table_sas: str=None
        ) -> None:
        super().__init__()
        if container_url is None and container_sas is None and table_url is None and table_sas is None:
            container_url = os.environ.get('AZURE_STORAGE_CONTAINER_URL')
            container_sas = os.environ.get('AZURE_STORAGE_CONTAINER_SAS')
            table_url = os.environ.get('AZURE_STORAGE_TABLE_URL')
            table_sas = os.environ.get('AZURE_STORAGE_TABLE_SAS')
        if container_url is not None and container_sas is not None:
            self.container_url = container_url
            from azure.storage.blob.aio import ContainerClient
            self.container_client = ContainerClient.from_container_url(container_url, credential=container_sas)
        if table_url is not None and table_sas is not None:
            self.table_url = table_url
            from azure.data.tables.aio import TableClient
            from azure.core.credentials import AzureSasCredential
            self.table_client = TableClient.from_table_url(table_url, credential=AzureSasCredential(table_sas))

    async def save_bytes(self, path: str, data: bytes, overwrite: bool=True) -> bool:
        # Check if the path exists and is a file
        if not overwrite:
            already_exist = await self.file_exists(path)
            if already_exist:
                return False
        # Upload data to the path, overwriting if necessary
        await self.container_client.upload_blob(name=path, data=data, overwrite=overwrite)
        return True
    
    async def read_all_bytes(self, path: str) -> bytes:
        # Download data from the path
        downloader = await self.container_client.download_blob(path)
        data = await downloader.readall()
        return data
    
    async def file_exists(self, path: str) -> bool:
        # Check if the path exists and is a file
        return await self.container_client.get_blob_client(path).exists()
    
    async def delete_file(self, path: str) -> bool:
        # Delete the path if it exists and is a file
        already_exist = await self.file_exists(path)
        if already_exist:
            await self.container_client.delete_blob(path)
            return True
        return False
    
    async def get_row(self, partition_key: str, row_key: str) -> dict:
        # Query the table
        return await self.table_client.get_entity(partition_key, row_key)
    
    async def query_rows(self, partition_key: str, row_start: str=None, row_end: str=None, top: int=None) -> AsyncIterable[dict]:
        # Query the table
        filter = f"PartitionKey eq '{partition_key}'"
        if row_start is not None:
            filter += f" and RowKey ge '{row_start}'"
        if row_end is not None:
            filter += f" and RowKey le '{row_end}'"
        args = {}
        if top is not None:
            args['results_per_page'] = top
        result = self.table_client.query_entities(query_filter=filter, **args)
        async for item in result:
            yield item
            if top is not None:
                top -= 1
                if top <= 0:
                    break

    async def upsert_row(self, entity: dict) -> None:
        # Insert the row
        await self.table_client.upsert_entity(entity)

    async def delete_row(self, entity: dict) -> None:
        # Delete the row
        await self.table_client.delete_entity(entity=entity)

