import re
import io
from typing import List
from urllib.parse import urlparse
from google.cloud import storage
from ..templates import StorageBase, DataUnit


class GCStorage(StorageBase):
    def __init__(self, project: str = None):
        self.storage_client = storage.Client(project=project)

    def ls(self, uri: str) -> List[DataUnit]:
        elements = self._list_blobs(uri=uri)
        return elements

    def save(self, data: bytes, uri: str) -> bool:
        done = self._upload_blob(data=data, uri=uri)
        return done

    def _parse_uri(self, uri: str):
        if uri[-1] == '/':
            uri = uri[:-1]

        p = urlparse(uri)

        if p.scheme != 'gs' or p.netloc == '':
            raise Exception('Invalid URI: %s' % uri)

        return p

    def _list_blobs(self, uri: str, delimiter='/') -> List[DataUnit]:
        parsed_url = self._parse_uri(uri)

        bucket_name = parsed_url.netloc
        prefix = parsed_url.path

        blobs = self.storage_client.list_blobs(
            bucket_name, prefix=prefix, delimiter=delimiter
        )

        path_objects = [DataUnit(name=blb.name,
                                 uri=uri + blb.name,
                                 is_folder=False)
                        for page in blobs.pages for blb in page]

        path_prefixes = [DataUnit(name=pref.replace(prefix, '')[:-1],
                                  uri=f"gs://{bucket_name}/{pref[:-1]}",
                                  is_folder=True)
                         for pref in blobs.prefixes]

        return path_objects + path_prefixes

    def _upload_blob(self, data: bytes, uri: str):
        bucket_name, relative_path = self._parse_uri(uri)

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(uri)

        f = io.BytesIO(data)
        f.seek(0)
        blob.upload_from_file(f)

        return True
