from pydantic import BaseModel


class StrategyDTO(BaseModel):
    symbol: str
    time_frame: float
    lot: float
    signal: str
    position: str


class BotDTO(BaseModel):
    bot_id: int
    strategy_dto: StrategyDTO
