from pydantic import BaseModel
from typing import Optional, List

class Keywords(BaseModel):
    id: int
    category_name: str
    tag: str
    keywords: List[str] = []
    max_size: int = 1000

