from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.routers.deps.client_session import HttpClientDep
import httpx2
import asyncio

pokemon_api_url="https://pokeapi.co/api/v2/pokemon/"

class PokemonService:
    def __init__(self, client: HttpClientDep):
        self.client = client
    async def get_pokemon(self, pokemon_id: int) -> dict:
        print(f"{pokemon_api_url}{pokemon_id}")
        response = await self.client.get(f"{pokemon_api_url}{pokemon_id}")
        response.raise_for_status()
        return response.json()
    async def get_pokemons(self, pokemon_list : list[int]):
        
        request = [self.get_pokemon(id) for id in pokemon_list]
        try:
            result_request = await asyncio.gather(*request)
            pokemon_list_name = [{"id":pokemon["id"], "name":pokemon["name"]} for pokemon in  result_request]
            return pokemon_list_name
        except httpx2.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error en una de las consultas externas: {exc.response.text}"
            )
        except httpx2.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Fallo de conexión con la API externa: {exc}"
            )

PokemonServiceDep = Annotated[PokemonService, Depends()]



