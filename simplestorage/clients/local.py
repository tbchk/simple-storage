import os
import glob
from typing import List
from ..templates import StorageBase, DataUnit


class LocalStorage(StorageBase):
    def ls(self, uri: str) -> List[DataUnit]:
        fpath = f"{uri}/*"
        matches = glob.glob(fpath)

        elements = [self._get_data_from_uri(uri=fpath)
                    for fpath in matches]

        return elements

    def save(self, data: bytes, uri: str):
        with open(uri, "wb") as f:
            f.write(data)

        return True

    def _get_data_from_uri(self, uri: str) -> DataUnit:
        name: str = os.path.basename(uri)
        is_folder: bool = os.path.isdir(uri)

        data = DataUnit(uri=uri, name=name, is_folder=is_folder)
        return data
