from os import environ
from fnmatch import fnmatch
from consul import Consul
from httpx import get
from typing import Dict, List, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import compile_path
from core_lib.consul import get_consul_service_url
from sessions import validate_session


ACCOUNT_SERVICE_NAME: str = environ["ACCOUNT_SERVICE_NAME"]
NOTIFICATION_SERVICE_NAME: str = environ["NOTIFICATION_SERVICE_NAME"]

PROTECTED_ROUTES: Dict[str, List[str]] = {}
INTERNAL_ROUTES: Dict[str, List[str]] = {}

CONSUL_HOST = environ["CONSUL_HOST"]
CONSUL_PORT = int(environ["CONSUL_PORT"])

consul_client = Consul(host=CONSUL_HOST, port=CONSUL_PORT)


async def fetch_routes() -> None:
    global PROTECTED_ROUTES, INTERNAL_ROUTES
    services = consul_client.catalog.services()[1].keys()
    for service in services:
        if service == "consul":
            continue
        service_url = get_consul_service_url(service)
        try:
            service_openapi = get(f"{service_url}/openapi.json").json()
            for path, methods in service_openapi["paths"].items():
                for _, details in methods.items():
                    if details.get("x-protected"):
                        if service not in PROTECTED_ROUTES:
                            PROTECTED_ROUTES[service] = []
                        PROTECTED_ROUTES[service].append(path)
                    if details.get("x-internal"):
                        if service not in INTERNAL_ROUTES:
                            INTERNAL_ROUTES[service] = []
                        INTERNAL_ROUTES[service].append(path)
        except Exception as e:
            print(f"Failed to fetch OpenAPI schema from {service}: {e}")


class AccessControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Any:
        if any(fnmatch(request.url.path, pattern) for pattern in INTERNAL_ROUTES):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"}
            )
        elif is_protected_route(path=request.url.path) and not await validate_session(
            request
        ):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Forbidden"}
            )
        response = await call_next(request)
        return response


def is_protected_route(path: str) -> bool:
    request_path = path

    path_parts = request_path.strip("/").split("/")
    if len(path_parts) < 2:
        remaining_path = "/" + "/".join(path_parts[1:])
    else:
        remaining_path = "/"

    service = path_parts[0]
    remaining_path = "/" + "/".join(path_parts[1:])
    if service in PROTECTED_ROUTES:
        for pattern in PROTECTED_ROUTES[service]:
            path_regex, _, _ = compile_path(pattern)
            if path_regex.match(remaining_path):
                return True

    return False
