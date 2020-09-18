import re
from typing import List
from glob import glob
import os
from abc import ABCMeta, abstractmethod

from google.cloud import storage


class StorageClient(object):
    def __init__(self, **args):

        # Services preconfigured
        self.gcs_service = None
        self.local_service = LocalStorage()

    def get_service(self, path: str):
        assert '/' in path, 'Malformed path'

        protocol = path.split('/')[0]

        if protocol == 'gs:':
            if not self.gcs_service:
                self.gcs_service = GCloudStorage()

            return self.gcs_service
        elif protocol == '':
            return self.local_service
        else:
            return None

    def ls(self, path: str) -> List[str]:
        service = self.get_service(path)

        if not service:
            raise Exception('Unknown service in path: %s' % path)

        listing = service.ls(path)
        return listing


class GCloudStorage(object):

    URI_REGEX = re.compile(r'[a-zA-Z]+://([a-z_-]*)/(.*)')

    def __init__(self):
        pass

    def uri_parser(self, path: str):

        results = re.findall(self.URI_REGEX, path)
        if len(results) == 0:
            raise Exception('Invalid URI: %s' % path)

        bucket, relative_path = results[0]
        return bucket, relative_path

    def ls(self, path: str):
        " path: absolute path on gcloud"
        bucket, relative_path = self.uri_parser(path)
        elements = self.list_blobs(bucket_name=bucket, prefix=relative_path)
        return elements

    def list_blobs(self, bucket_name: str, prefix: str, delimiter='/'):
        storage_client = storage.Client(project='guaneenergy')

        blobs = storage_client.list_blobs(
            bucket_name, prefix=prefix, delimiter=delimiter
        )

        path_objects = [Element(name=b.name, uri=b.uri, is_folder=False)
                        for page in blobs.pages for b in page]

        path_prefixes = [
            Element(
                name=pref.replace(prefix, ''), uri=f"gs://{bucket_name}/{pref}",
                is_folder=True)
            for pref in blobs.prefixes]

        return path_objects + path_prefixes


class LocalStorage(object):
    def __init__(self):
        pass

    def ls(self, path: str):
        fpath = f"{path}/*"
        matches = glob(fpath)

        elements = [
            Element(
                name=fname.replace(path, ""),
                uri=fname,
                is_folder=os.path.isdir(fname))
            for fname in matches]

        return elements


class Element(object):

    def __init__(self, name: str, uri: str, is_folder: str, 
            content_bytes: bytes = None):

        self.name = name
        self.uri = uri
        self.is_folder = is_folder
        self.content_bytes = content_bytes

    def __repr__(self):
        fold = 'd' if self.is_folder else '-'

        representation = f"{fold} {self.name}"
        return representation

    def is_loaded(self):
        if self.content_bytes is None:
            return False
        else:
            return True
