from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel
from app.config.db import engine
import app.models
from contextlib import asynccontextmanager
from typing import Annotated
import httpx2
from app.routers.user_router import user_router
from app.routers.deps.client_session import HttpClientDep
SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx2.AsyncClient(
        timeout=httpx2.Timeout(10.0),
        headers={"Accept": "application/json"}
    )
    yield
    # Se cierran las conexiones limpiamente al apagar el servidor
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
app.include_router(user_router)

