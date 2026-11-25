from sqlmodel import SQLModel, Field
from sqlalchemy import ARRAY, Column, Integer, JSON

class UserBase(SQLModel):
    username: str = Field()
    email: str = Field()
    password: str = Field()
    pokemonId : list[int] = Field(default_factory=list, sa_column=Column(ARRAY(Integer).with_variant(JSON, "sqlite")))

class UserCreateIn(UserBase):...

class UserCreateOut(SQLModel):
    id: int = Field()

class User(UserBase, table=True):
    id: int = Field(primary_key=True)

class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    pokemonId : list[int] | None

class UserPokemon(UserBase):
    list_pokemon : list[dict] = Field()