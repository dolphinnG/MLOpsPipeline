import json
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from services.implementations.LDAPService import LDAPService
from services.interfaces.IUserService import IUserService
from models.userModel import UserCreate, UserRead, UserUpdate
from typing import List
from dependencies.deps import get_ldap_service

router = APIRouter()

templates = Jinja2Templates(directory="templates")
# Add custom filter to Jinja2 templates
templates.env.filters['load_json'] = json.loads

@router.get("/create")
async def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@router.post("/action/", response_model=dict)
async def create_user(user: UserCreate, ldap_service: IUserService = Depends(get_ldap_service)):
    async with ldap_service.create_conn() as conn:
        result = await conn.add_user(user)
        if result['description'] != 'success':
            raise HTTPException(status_code=400, detail="Failed to create user")
        result = await conn.add_user_to_group(user.uid, user.group)
        if result['description'] != 'success':
            raise HTTPException(status_code=400, detail="Failed to add user to group")
        return {"message": "User created successfully"}

@router.put("/action/{user_dn}", response_model=dict)
async def update_user(user_dn: str, user: UserUpdate, ldap_service: IUserService = Depends(get_ldap_service)):
    async with ldap_service.create_conn() as conn:
        result = await conn.update_user(user_dn, user)
        if result['description'] != 'success':
            raise HTTPException(status_code=400, detail="Failed to update user")
        return {"message": "User updated successfully"}

@router.delete("/action/{user_dn}", response_model=dict)
async def delete_user(user_dn: str, ldap_service: IUserService = Depends(get_ldap_service)):
    async with ldap_service.create_conn() as conn:
        result = await conn.delete_user(user_dn)
        if result['description'] != 'success':
            raise HTTPException(status_code=400, detail="Failed to delete user")
        return {"message": "User deleted successfully"}

@router.get("/action/{user_dn}", response_model=List[UserRead])
async def get_user(user_dn: str, ldap_service: IUserService = Depends(get_ldap_service)):
    async with ldap_service.create_conn() as conn:
        users = await conn.get_users(user_dn=user_dn)
        return users

@router.get("/action/", response_model=List[UserRead])
async def get_all_users(ldap_service: IUserService = Depends(get_ldap_service)):
    async with ldap_service.create_conn() as conn:
        users = await conn.get_users()
        return users
    
@router.get("/groups/", response_model=List[str])
async def get_all_groups(ldap_service: IUserService = Depends(get_ldap_service)):
    async with ldap_service.create_conn() as conn:
        groups = await conn.get_all_groups()
        return groups

