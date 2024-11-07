from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class ICacheService(ABC):
    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key) -> Any:
        pass

    @abstractmethod
    def set_pydantic_cache(self, key: str, model: BaseModel):
        pass

    @abstractmethod
    def get_pydantic_cache(self, key: str, model_class: Type[T]) -> T|None:
        pass

    @abstractmethod
    def invalidate(self, key: str):
        pass
