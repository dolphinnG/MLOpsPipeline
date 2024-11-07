import redis
import logging
from typing import Type, TypeVar
from pydantic import BaseModel
from services.interfaces.ICacheService import ICacheService

T = TypeVar('T', bound=BaseModel)

class RedisService(ICacheService):
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.logger = logging.getLogger(__name__)

    def set(self, key, value):
        try:
            self.client.set(key, value)
        except Exception as e:
            self.logger.error(f"Error setting key {key}: {e}")

    def get(self, key):
        try:
            value = self.client.get(key)
            return value
        except Exception as e:
            self.logger.error(f"Error getting key {key}: {e}")

    def set_pydantic_cache(self, key: str, model: BaseModel):
        try:
            self.client.set(key, model.model_dump_json())
        except Exception as e:
            self.logger.error(f"Error setting model for key {key}: {e}")

    def get_pydantic_cache(self, key: str, model_class: Type[T]) -> T|None:
        try:
            value = self.client.get(key)
            if value:
                return model_class.model_validate_json(value) # type: ignore
            return None
        except Exception as e:
            self.logger.error(f"Error getting model for key {key}: {e}")
            return None

    def invalidate(self, key: str):
        try:
            self.client.delete(key)
        except Exception as e:
            self.logger.error(f"Error invalidating key {key}: {e}")

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