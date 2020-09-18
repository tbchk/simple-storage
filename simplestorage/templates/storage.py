from abc import ABCMeta, abstractmethod
from typing import List
from data import DataUnit


class StorageBase(metaclass=ABCMeta):
    @abstractmethod
    def ls(self, uri: str) -> List[DataUnit]:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: bytes, uri: str):
        raise NotImplementedError
