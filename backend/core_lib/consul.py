from os import environ
from consul import Consul, Check
from fastapi import HTTPException
from tenacity import retry, stop_after_attempt, wait_exponential

# TODO SHOWS RECEIVE THESE FROM CONSUMER CODE AND NOT get them directly.
SERVICE_NAME = environ["SERVICE_NAME"]
SERVICE_ID = environ["SERVICE_ID"]
SERVICE_HOST = environ["SERVICE_HOST"]
SERVICE_PORT = int(environ["SERVICE_PORT"])
CONSUL_HOST = environ["CONSUL_HOST"]
CONSUL_PORT = int(environ["CONSUL_PORT"])


consul_client = None


def initialize_consul_client():
    global consul_client
    if consul_client is None:
        consul_client = Consul(host=CONSUL_HOST, port=CONSUL_PORT)


@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=10))
def register_service():
    global consul_client
    consul_client = Consul(host=CONSUL_HOST, port=CONSUL_PORT)
    consul_client.agent.service.register(
        name=SERVICE_NAME,
        service_id=SERVICE_ID,
        address=SERVICE_HOST,
        port=SERVICE_PORT,
        check=Check().tcp(SERVICE_HOST, SERVICE_PORT, "10s"),
    )


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_consul_service_url(service_name: str, wsurl: bool = False) -> str:
    initialize_consul_client()
    global consul_client
    if not consul_client:
        raise ValueError("Consul client is not initialized")
    services = consul_client.catalog.service(service_name)[1]
    if not services:
        raise HTTPException(status_code=500, detail=f"Service {service_name} not found")
    service = services[0]
    if wsurl:
        return f"ws://{service['ServiceAddress']}:{service['ServicePort']}/ws"
    return f"http://{service['ServiceAddress']}:{service['ServicePort']}"
