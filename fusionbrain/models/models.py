from typing import Dict, Any

from dataclasses import dataclass


@dataclass
class ModelModel:
    id: int
    name: str
    version: float
    type: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelsItem":
        return cls(**data)

