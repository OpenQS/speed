from typing import Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from .lattice import Lattice
from .problems import Problem


# Predefined architectures
class Architecture(str, Enum):
    GPU_A100 = "GPU:A100"
    GPU_H100 = "GPU:H100"
    GPU_V100 = "GPU:V100"
    GPU_RTX4090 = "GPU:RTX4090"
    GPU_RTX3090 = "GPU:RTX3090"
    GPU_RTX4080 = "GPU:RTX4080"
    GPU_RTX3080 = "GPU:RTX3080"
    GPU_MI250X = "GPU:MI250X"
    GPU_MI300X = "GPU:MI300X"
    CPU_i7_14100 = "CPU:i7-14100"
    CPU_i9_14900K = "CPU:i9-14900K"
    CPU_i5_13600K = "CPU:i5-13600K"
    CPU_Xeon_8375C = "CPU:Xeon-8375C"
    CPU_Xeon_8480 = "CPU:Xeon-8480"
    CPU_EPYC_7763 = "CPU:EPYC-7763"
    CPU_EPYC_9654 = "CPU:EPYC-9654"
    CPU_M2_Max = "CPU:M2-Max"
    CPU_M3_Max = "CPU:M3-Max"
    CPU_M1_Ultra = "CPU:M1-Ultra"
    TPU_v4 = "TPU:v4"
    TPU_v5 = "TPU:v5"


# Discriminated union on `name`

class DataModel(BaseModel):
    problem: Problem
    N: int
    time: float
    architecture: Annotated[
        str,
        Field(
            description="Hardware architecture (select from predefined list or enter custom)",
            examples=[arch.value for arch in Architecture]
        )
    ]
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