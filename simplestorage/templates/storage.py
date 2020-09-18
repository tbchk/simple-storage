from abc import ABCMeta, abstractmethod
from typing import List


class StorageBase(metaclass=ABCMeta):
    @abstractmethod
    def ls(self, uri: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: bytes, uri: str) -> bool:
        raise NotImplementedError
