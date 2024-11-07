from fastapi import Request, Response

class IAuthService:
    async def login(self, response: Response):
        raise NotImplementedError

    async def callback(self, request: Request, code: str, state: str):
        raise NotImplementedError

    async def logout(self, request: Request, response: Response):
        raise NotImplementedError

    async def validate_token(self, request: Request):
        raise NotImplementedError
