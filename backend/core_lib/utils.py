from httpx import AsyncClient, HTTPError
from pydantic import TypeAdapter
from typing import Type, TypeVar
from fastapi import HTTPException, status


T = TypeVar("T")


async def fetch(url: str, response_type: Type[T], **kwargs) -> T:
    async with AsyncClient() as client:
        try:
            response = await client.post(url, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                value = TypeAdapter(response_type).validate_python(response.json())
                return value
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        
    
