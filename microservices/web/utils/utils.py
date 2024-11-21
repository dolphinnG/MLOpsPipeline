import os
import base64
import hashlib

from fastapi import Request
from fastapi.responses import StreamingResponse
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
    headers = dict(request.headers)
    params = dict(request.query_params)
    body = await request.body()
    response = await httpx_client.request(
        method=request.method, url=url, headers=headers, params=params, content=body
    )
    # Return the response from the target microservice
    return response


async def proxy_to_model_management(
    request: Request, httpx_client: AsyncClient, path: str
):
    model_management_host = "http://localhost:15000/mlflow"
    res = await proxy_request(request, httpx_client, model_management_host, path)
    return res.json()


async def proxy_to_orchestration(
    request: Request, httpx_client: AsyncClient, path: str
):
    orchestration_host = "http://localhost:15001/api/v1"
    res = await proxy_request(request, httpx_client, orchestration_host, path)
    return res.json()


async def proxy_to_jobs_monitor(request: Request, httpx_client: AsyncClient, path: str):
    jobs_monitor_host = "http://localhost:15002/distributed"
    res = await proxy_request(request, httpx_client, jobs_monitor_host, path)
    return res.json()


async def proxy_to_launcher(request: Request, httpx_client: AsyncClient, path: str):
    jobs_monitor_host = "http://localhost:15003/launcher"
    res = await proxy_request(request, httpx_client, jobs_monitor_host, path)
    return res.json()


async def proxy_text_stream(
    request: Request, httpx_client: AsyncClient, microservice: str, path: str
):
    url = f"{microservice}/{path}"
    headers = dict(request.headers)
    params = dict(request.query_params)
    body = await request.body()

    async def stream_content():
        async with httpx_client.stream(
            method=request.method,
            url=url,
            headers=headers,
            params=params,
            content=body,
            timeout=100.0,
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_text():
                yield chunk

    return StreamingResponse(stream_content(), media_type="text/plain")


async def proxy_stream_to_launcher(
    request: Request, httpx_client: AsyncClient, path: str
):
    jobs_monitor_host = "http://localhost:15003/launcher"
    stream = await proxy_text_stream(request, httpx_client, jobs_monitor_host, path)
    return stream
