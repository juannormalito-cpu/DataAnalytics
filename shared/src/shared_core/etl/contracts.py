from abc import ABC, abstractmethod
from typing import Any


class Extractor(ABC):
    @abstractmethod
    def extract(self) -> Any: ...


class Transformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> Any: ...


class Loader(ABC):
    @abstractmethod
    def load(self, data: Any) -> None: ...
