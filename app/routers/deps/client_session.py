from typing import Annotated
import httpx2
from fastapi import Depends, Request

def get_http_client(request: Request) -> httpx2.AsyncClient:
    return request.app.state.http_client

HttpClientDep = Annotated[httpx2.AsyncClient, Depends(get_http_client)]