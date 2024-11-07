from abc import ABC, abstractmethod
from services.implementations import LDAPService

class IUserService(ABC):
    
    @abstractmethod
    def create_conn(self) -> 'LDAPService.LDAPService.LDAPConn':
        pass
    
    # @abstractmethod
    # async def __aenter__(self) -> Any:
    #     pass

    # @abstractmethod
    # async def __aexit__(self, exc_type, exc_value, traceback):
    #     pass

    # @abstractmethod
    # async def add_user(self, user: UserCreate):
    #     pass

    # @abstractmethod
    # async def update_user(self, user_dn: str, user: UserUpdate):
    #     pass

    # @abstractmethod
    # async def delete_user(self, user_dn: str):
    #     pass

    # @abstractmethod
    # async def add_user_to_group(self, user_dn: str, group_dn: str):
    #     pass

    # @abstractmethod
    # async def remove_user_from_group(self, user_dn: str, group_dn: str):
    #     pass

    # @abstractmethod
    # async def get_users(self, user_dn: str) -> Any:
    #     pass

    # @abstractmethod
    # async def get_all_groups(self) -> Any:
    #     pass
