import os
import base64
import hashlib

from fastapi import Request
from httpx import AsyncClient

from models.userModel import UserRead


def generate_code_verifier():
    return os.urandom(40).hex()


def generate_code_challenge(code_verifier):
    return (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )


def ldap_entry_to_dict(entry_with_group):  # cant do model_validate_json
    entry = entry_with_group[0]
    groups = entry_with_group[1]
    return UserRead(
        name=entry["cn"].value,
        mail=entry["mail"].value,
        title=entry["title"].value,
        location=entry["l"].value,
        telephoneNumber=entry["telephoneNumber"].value,
        groups=groups,
        uid=entry["uid"].value,
    )


async def proxy_request(
    request: Request, httpx_client: AsyncClient, microservice: str, path: str
):
    url = f"{microservice}/{path}"

    # Forward the request headers
    headers = dict(request.headers)

    # Forward the query parameters
    params = dict(request.query_params)

    # Forward the request body
    body = await request.body()

    # Make the request to the target microservice
    response = await httpx_client.request(
        method=request.method, url=url, headers=headers, params=params, content=body
    )

    # Return the response from the target microservice
    return response


async def proxy_to_model_management(
    request: Request, httpx_client: AsyncClient, path: str
):
    model_management_host = "http://localhost:15000/mlflow"
    res =  await proxy_request(request, httpx_client, model_management_host, path)
    return res.json()