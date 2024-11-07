from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    cn: str
    sn: str
    uid: str
    mail: EmailStr
    userPassword: str
    title: Optional[str] = None
    l: Optional[str] = None
    telephoneNumber: Optional[str] = None

class UserCreate(UserBase):
    objectClass: list = ['inetOrgPerson']

class UserUpdate(BaseModel):
    cn: Optional[str] = None
    sn: Optional[str] = None
    mail: Optional[EmailStr] = None
    userPassword: Optional[str] = None
    title: Optional[str] = None
    l: Optional[str] = None
    telephoneNumber: Optional[str] = None
    
class UserRead(BaseModel):
    name: str
    mail: EmailStr
    title: str
    location: str
    telephoneNumber: str
    groups: list = []
    uid: str

