import re
import io
from typing import List
from google.cloud import storage
from ..templates import StorageBase, DataUnit


class GCStorage(StorageBase):
    URI_REGEX = re.compile(r'[a-zA-Z]+://([a-z_-]*)/(.*)')

    def __init__(self, project: str = None):
        self.storage_client = storage.Client(project=project)

    def ls(self, uri: str) -> List[DataUnit]:
        elements = self._list_blobs(uri=uri)
        return elements

    def save(self, data: bytes, uri: str) -> bool:
        done = self._upload_blob(data=data, uri=uri)
        return done

    def _parse_uri(self, uri: str):
        results = re.findall(self.URI_REGEX, uri)
        if len(results) == 0:
            raise Exception('Invalid URI: %s' % uri)

        bucket, relative_path = results[0]
        return bucket, relative_path

    def _list_blobs(self, uri: str, delimiter='/') -> List[DataUnit]:
        bucket_name, relative_path = self._parse_uri(uri)
        blobs = self.storage_client.list_blobs(
            bucket_name, prefix=relative_path, delimiter=delimiter
        )

        path_objects = [DataUnit(name=blb.name, uri=blb.uri, is_folder=False)
                        for page in blobs.pages for blb in page]

        path_prefixes = [DataUnit(name=pref.replace(relative_path, ''),
                                  uri=f"gs://{bucket_name}/{pref}",
                                  is_folder=True)
                         for pref in blobs.prefixes]

        return path_objects + path_prefixes

    def _upload_blob(self, data: bytes, uri: str):
        bucket_name, relative_path = self._parse_uri(uri)

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(uri)

        f = io.BytesIO(data)
        blob.upload_from_file(f)

        return True
