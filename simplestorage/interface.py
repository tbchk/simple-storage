from typing import List
from clients import LocalStorage, GCStorage
from templates import DataUnit, StorageBase


class StorageInterface(StorageBase):

    def __init__(self):
        self.local_service = None
        self.gcs_service = None

    def _get_service(self, uri: str):
        assert '/' in uri, 'Malformed path'
        protocol = uri.split('/')[0]

        if protocol == 'gs:':
            if not self.gcs_service:
                self.gcs_service = GCStorage()

            return self.gcs_service
        elif protocol == '':
            if not self.local_service:
                self.local_service = LocalStorage()
            return self.local_service
        else:
            raise Exception('Unknown service in path: %s' % uri)

    def ls(self, uri: str) -> List[DataUnit]:
        service = self._get_service(uri)
        listing = service.ls(uri=uri)
        return listing

    def save(self, data: bytes, uri: str) -> bool:
        service = self._get_service(uri)
        status = service.save(data=data, uri=uri)
        return status
