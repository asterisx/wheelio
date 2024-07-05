from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def generate_custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Notification Service",
        version="0.0.1",
        description="The notification service",
        routes=app.routes,
    )
    if "/ws" not in openapi_schema["paths"]:
        openapi_schema["paths"]["/ws"] = {
            "get": {
                "summary": "WebSocket endpoint",
                "description": "WebSocket connection endpoint",
                "responses": {
                    "200": {
                        "description": "Successful connection",
                    }
                },
            }
        }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
