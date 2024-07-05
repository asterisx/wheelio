from os import environ
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from sessions import create_session
from core_lib.consul import get_consul_service_url

ACCOUNT_SERVICE_NAME: str = environ["ACCOUNT_SERVICE_NAME"]


async def login(user: dict) -> Response:
    account_service_url = get_consul_service_url(ACCOUNT_SERVICE_NAME)
    async with AsyncClient() as client:
        response = await client.post(f"{account_service_url}/login", json=user)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code, detail=response.json().get("detail")
            )
        session_token = create_session(user.get("username"))
        fastapi_response = JSONResponse(
            content=response.json(), status_code=response.status_code
        )
        fastapi_response.set_cookie(
            key="session_token", value=session_token, samesite="Strict", secure=True
        )
        return fastapi_response


async def logout() -> Response:
    account_service_url = get_consul_service_url(ACCOUNT_SERVICE_NAME)
    async with AsyncClient() as client:
        response = await client.post(f"{account_service_url}/logout")
        fastapi_response = JSONResponse(
            content=response.json(), status_code=response.status_code
        )
        fastapi_response.delete_cookie(key="session_token")
        return fastapi_response
