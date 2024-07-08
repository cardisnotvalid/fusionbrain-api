from typing import Dict, Any

from dataclasses import dataclass


@dataclass
class GenerateModel:
    uuid: int
    status: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GenerateModel":
        return cls(**data)

