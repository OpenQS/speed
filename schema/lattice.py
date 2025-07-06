from typing import Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field, field_validator

class BaseLattice(BaseModel):
    name : str

class Chain(BaseLattice):
    name : Literal["Chain"]
    L: int
    pbc: bool 

class Square(BaseLattice):
    name : Literal["Square"]
    L: int
    pbc: bool

class Rectangular(BaseLattice):
    name : Literal["Rectangular"]
    Lx: int
    Ly: int
    pbc: bool

class Triangular(BaseLattice):
    name : Literal["Triangular"]
    L: int

class Kagome(BaseLattice):
    name : Literal["Kagome"]
    L: int

class Honeycomb(BaseLattice):
    name : Literal["Honeycomb"]
    L: int

class Cubic(BaseLattice):
    name : Literal["Cubic"]
    L: int

Lattice = Annotated[
    Union[Chain, Square, Rectangular, Triangular, Kagome, Honeycomb, Cubic],
    Field(discriminator="name")
]
