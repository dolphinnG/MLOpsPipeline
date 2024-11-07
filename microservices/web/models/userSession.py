from pydantic import BaseModel
from typing import Optional, Dict

class UserSession(BaseModel):
    code_verifier: str
    state: str
    nonce: str
    access_token: str | None = None
    refresh_token: str | None = None
    ldapGroup: list[str] | None = None
    decoded_id_token: Dict[str, str|int|list] | None = None
    decoded_access_token: Dict[str, str|int|list] | None = None
