from pydantic import BaseModel
from typing import List


class PositionDTO(BaseModel):
    type: str
    profit: float


class BotDTO(BaseModel):
    name: str
    positions: List[PositionDTO]
    online: bool
