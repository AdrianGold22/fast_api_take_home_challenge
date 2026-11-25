from fastapi import APIRouter, HTTPException, Query
from app.models.user import User, UserCreateIn, UserCreateOut, UserUpdate, UserPokemon
from app.routers.deps.db_session import SessionDep
from sqlmodel import Session,select
from app.routers.deps.client_session import HttpClientDep
from app.services.pokemon_service import PokemonService, PokemonServiceDep
from typing import Annotated
user_router = APIRouter(prefix="/users", tags=["user"])

@user_router.get("/")
def get_items(db: SessionDep)->list[User]:
    statement= select(User)
    result = db.exec(statement).all()
    return result

@user_router.post("/")
def add_items(item: UserCreateIn, db:SessionDep)->UserCreateOut:
    db_item=User(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return UserCreateOut(id=db_item.id)

@user_router.get("/{id}")
async def get_item(id : int, db:SessionDep, service:PokemonServiceDep)-> UserPokemon | None:
    db_user = db.get(User,id)
    if not db_user:
        return None
    list_pokemon = await service.get_pokemons(db_user.pokemonId)
    user_complete = UserPokemon(**db_user.model_dump(), list_pokemon=list_pokemon)
    return user_complete

@user_router.delete("/")
def delete_item(id:int, db:SessionDep):
    db_user = db.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

@user_router.put("/")
def update_item(id : int, user: UserUpdate, db: SessionDep):
    db_user = db.get(User, id)
    if not db_user:
        return HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


