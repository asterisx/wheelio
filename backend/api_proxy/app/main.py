from os import environ
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from core_lib.consul import get_consul_service_url
from dependencies import AccessControlMiddleware, fetch_routes
from sessions import get_current_username
from custom_openapi_factory import custom_openapi_factory
from auth import login, logout

ACCOUNT_SERVICE_NAME = environ["ACCOUNT_SERVICE_NAME"]
NOTIFICATION_SERVICE_NAME = environ["NOTIFICATION_SERVICE_NAME"]
FRONTEND_ORIGIN = environ["FRONTEND_ORIGIN"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    await fetch_routes()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AccessControlMiddleware)


@app.middleware("http")
async def add_current_username(request: Request, call_next):
    current_user_name = await get_current_username(request=request)
    request.state.current_user_name = current_user_name
    response = await call_next(request)
    return response


async def event_stream(request: Request):
    service_url = get_consul_service_url(NOTIFICATION_SERVICE_NAME)
    current_user_name = request.state.current_user_name
    headers = dict(request.headers)
    if current_user_name:
        headers["X-Current-User-Name"] = current_user_name
    async with AsyncClient(timeout=None) as client:
        async with client.stream(
            request.method, service_url, params=request.query_params, headers=headers
        ) as stream:
            try:
                async for log_line in stream.aiter_text():
                    if await request.is_disconnected():
                        break
                    if "ping" not in log_line:
                        yield log_line

            finally:
                await stream.aclose()


async def notification_sse(request: Request):
    return EventSourceResponse(event_stream(request))


@app.api_route(
    "/{service_name}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    include_in_schema=False,
)
async def proxy_request(service_name: str, path: str, request: Request):
    if service_name == ACCOUNT_SERVICE_NAME and path == "login":
        return await login(await request.json())
    if service_name == ACCOUNT_SERVICE_NAME and path == "logout":
        return await logout()
    service_url = get_consul_service_url(service_name)
    url = f"{service_url}/{path}"
    current_user_name = request.state.current_user_name
    headers = dict(request.headers)
    if current_user_name:
        headers["X-Current-User-Name"] = current_user_name
    if service_name == NOTIFICATION_SERVICE_NAME:
        request.state.headers = headers
        return await notification_sse(request)

    else:
        async with AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
            )
            return JSONResponse(
                content=response.json(), status_code=response.status_code
            )


app.openapi = custom_openapi_factory(app)
