from fastapi import Request, Response

class IAuthService:
    def login(self, response: Response):
        raise NotImplementedError

    def callback(self, request: Request, code: str, state: str):
        raise NotImplementedError

    def logout(self, request: Request, response: Response):
        raise NotImplementedError

    def validate_token(self, request: Request):
        raise NotImplementedError
