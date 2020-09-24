from pydantic import BaseModel

class Arbitrage(BaseModel):
    position_ratio: int = 0.015
    resolution_ratio: int = 0.015 / 1.8