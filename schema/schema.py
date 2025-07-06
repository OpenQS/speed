from typing import Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field, field_validator

from .lattice import Lattice
from .problems import Problem


# Discriminated union on `name`

class DataModel(BaseModel):
    problem: Problem
    N: int
    time: float
    architecture: str
    doi: Annotated[
        str,
        Field(
        min_length=10,
        pattern=r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$"
        )]    
    extra: Optional[str] = None

    @field_validator("N")
    @classmethod
    def check_N_int32(cls, v: int) -> int:
        if not 1 <= v < 2**31:
            raise ValueError("N must fit in signed 32-bit integer")
        return v