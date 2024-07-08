from typing import Optional, Dict, List, Any

from dataclasses import dataclass


@dataclass
class StatusModel:
    uuid: int
    status: str
    censored: str
    generation_time: Optional[int] = None
    image: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StatusModel":
        return cls(
            generation_time=data.pop("generationTime", None),
            image=data.pop("images", [None])[0],
            error=data.pop("errorDescription", None), 
            **data,
        )

