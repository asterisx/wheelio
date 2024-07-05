from os import environ
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from typing import Dict
from requests import get
from consul import Consul
from core_lib.consul import get_consul_service_url

CONSUL_HOST = environ["CONSUL_HOST"]
CONSUL_PORT = int(environ["CONSUL_PORT"])

consul_client = Consul(host=CONSUL_HOST, port=CONSUL_PORT)


def custom_openapi_factory(app: FastAPI):
    def custom_openapi() -> Dict[str, any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="API",
            version="0.0.1",
            description="API",
            routes=app.routes,
        )
        services = consul_client.catalog.services()[1].keys()
        for service in services:
            if service == "consul":
                continue
            service_url = get_consul_service_url(service)
            try:
                service_openapi = get(f"{service_url}/openapi.json").json()
                openapi_schema.setdefault("components", {})
                if "components" in service_openapi:
                    if "components" not in openapi_schema:
                        openapi_schema["components"] = {}
                    for component_type, components in service_openapi[
                        "components"
                    ].items():
                        if component_type not in openapi_schema["components"]:
                            openapi_schema["components"][component_type] = {}
                        openapi_schema["components"][component_type].update(components)
                for path, path_item in service_openapi["paths"].items():
                    modified_path = f"/{service}{path}"
                    openapi_schema["paths"][modified_path] = path_item

            except Exception as e:
                print(f"Failed to fetch OpenAPI schema from {service}: {e}")

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi
