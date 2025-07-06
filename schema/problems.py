from typing import Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field, field_validator

from .lattice import Lattice

class BaseProblem(BaseModel):
    name: str
    Lattice: Lattice

# Each variant of Problem
class HeisenbergProblem(BaseProblem):
    # J = 1.0
    name: Literal["Heisenberg"]

class J1J2Problem(BaseProblem):
    # J1 = 1.0
    name: Literal["J1-J2"]
    J2: float

class HubbardProblem(BaseProblem):
    # t = 1
    name: Literal["Hubbard"]
    U: float

class IsingProblem(BaseProblem):
    name: Literal["Ising"]
    h: float

Problem = Annotated[
    Union[HeisenbergProblem, IsingProblem, J1J2Problem, HubbardProblem],
    Field(discriminator="name")
]
