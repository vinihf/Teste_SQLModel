'''from fastapi import FastAPI
from typing import Optional
from sqlmodel import Field, SQLModel,Relationship, create_engine, Session, select

class pokemon(SQLModel, table=True):
    Pokedex_number: Optional[int] = Field(default=None, primary_key=True)
    Name: str
    is_legendary: int
    Defense: int
    Attack: int
    type: int = Field(foreign_key="type.id_type")
    type_all: type = Relationship(back_populates="pokemons")


class type(SQLModel, table=True):
    id_type:  Optional[int] = Field(default=None, primary_key=True)
    text: str
    pokemons: list["pokemon"] = Relationship(back_populates="type_all")

engine = create_engine("mysql://root:@localhost:3306/pokemons_dataset", echo=True)

def get_all():
    with Session(engine) as session:
        statement = select(pokemon)
        results = session.exec(statement)
        return results

app = FastAPI()


@app.get("/", response_model=list[pokemon])
async def root():
    get_all()


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
'''
from fastapi import FastAPI
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session, select
from sqlalchemy.orm import joinedload

class Pokemon(SQLModel, table=True):
    Pokedex_number: Optional[int] = Field(default=None, primary_key=True)
    Name: str
    is_legendary: int
    Defense: int
    Attack: int
    type_id: int = Field(foreign_key="type.id_type")
    type_all: "Type" = Relationship(back_populates="pokemons")

class Type(SQLModel, table=True):
    id_type: Optional[int] = Field(default=None, primary_key=True)
    text: str
    pokemons: list["Pokemon"] = Relationship(back_populates="type_all")

engine = create_engine("mysql://root:@localhost:3306/pokemons_dataset", echo=True)

def get_all():
    with Session(engine) as session:
        statement = select(Pokemon)
        results = session.exec(statement)
        return results.all()

def get_id(id:int):
    with Session(engine) as session:
        statement = select(Pokemon).options(joinedload(Pokemon.type_all)).where(Pokemon.Pokedex_number == id)
        result = session.exec(statement)
        return result.one()
app = FastAPI()

@app.get("/")
async def root():
    return get_all()  # Corrigir para retornar o valor da função

@app.get("/{id:int}")
async def root_get(id: int):
    return get_id(id)
