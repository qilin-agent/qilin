from qilin.utils.storage.storageabc import Storage


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
