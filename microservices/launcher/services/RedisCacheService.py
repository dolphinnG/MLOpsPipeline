import json
import redis
import logging
from typing import Sequence, Type, TypeVar
from pydantic import BaseModel
from .ICacheService import ICacheService

T = TypeVar('T', bound=BaseModel)

class RedisService(ICacheService):
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.logger = logging.getLogger(__name__)

    async def set(self, key, value):
        try:
            self.client.set(key, value)
        except Exception as e:
            self.logger.error(f"Error setting key {key}: {e}")

    async def get(self, key):
        try:
            value = self.client.get(key)
            return value
        except Exception as e:
            self.logger.error(f"Error getting key {key}: {e}")

    async def set_pydantic_cache(self, key: str, model: BaseModel):
        try:
            self.client.set(key, model.model_dump_json())
        except Exception as e:
            self.logger.error(f"Error setting model for key {key}: {e}")

    async def get_pydantic_cache(self, key: str, model_class: Type[T]) -> T|None:
        try:
            value = self.client.get(key)
            if value:
                return model_class.model_validate_json(value) # type: ignore
            return None
        except Exception as e:
            self.logger.error(f"Error getting model for key {key}: {e}")
            return None
    
    async def invalidate(self, key: str):
        try:
            self.client.delete(key)
        except Exception as e:
            self.logger.error(f"Error invalidating key {key}: {e}")

    async def set_pydantic_list_cache(self, key: str, model_list: Sequence[BaseModel]):
        try:
            model_dicts = [model.model_dump() for model in model_list]
            model_list_json = json.dumps(model_dicts)
            await self.set(key, model_list_json)
        except Exception as e:
            self.logger.error(f"Error setting model list for key {key}: {e}")
            
    async def get_pydantic_list_cache(self, key: str, model_class: Type[T]) -> list[T]:
        try:
            value = await self.get(key)
            assert isinstance(value, str), "Cached value is not a string"
            if value:
                model_dicts = json.loads(value)
                return [model_class(**model_dict) for model_dict in model_dicts]
            return []
        except Exception as e:
            self.logger.error(f"Error getting model list for key {key}: {e}")
            return []
# # Example usage
# if __name__ == "__main__":
#     from pydantic import BaseModel
#
#     class ExampleModel(BaseModel):
#         name: str
#         age: int
#
#     repo = RedisRepository()
#     example_model = ExampleModel(name="John", age=30)
#     repo.set_model("example_model", example_model)
#     retrieved_model = repo.get_model("example_model", ExampleModel)
#     print(f"Retrieved model: {retrieved_model}")
#     repo.invalidate("example_model")
#     invalidated_model = repo.get_model("example_model", ExampleModel)
#     print(f"Invalidated model: {invalidated_model}")