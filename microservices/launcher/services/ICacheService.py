from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Sequence
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class ICacheService(ABC):
    @abstractmethod
    async def set(self, key, value):
        pass

    @abstractmethod
    async def get(self, key) -> Any:
        pass

    @abstractmethod
    async def set_pydantic_cache(self, key: str, model: BaseModel):
        pass

    @abstractmethod
    async def get_pydantic_cache(self, key: str, model_class: Type[T]) -> T|None:
        pass

    @abstractmethod
    async def invalidate(self, key: str):
        pass

    @abstractmethod
    async def set_pydantic_list_cache(self, key: str, model_list: Sequence[BaseModel]):
        pass

    @abstractmethod
    async def get_pydantic_list_cache(self, key: str, model_class: Type[T]) -> list[T]:
        pass
