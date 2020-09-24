from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from magnet.database import get_db
from sqlalchemy.orm import Session
from libs import generator
from fastapi.responses import PlainTextResponse
import ast
import json
import hjson

router = APIRouter()

@router.post("/json_to_pydantic", response_class=PlainTextResponse)
async def json_to_pydantic(json: str = "{}"):
    dic = hjson.loads(json)

    model_name = "Dummy"
    code = generator.dump_pydantic_code_from_json(
        __model_name=model_name,
        data=dic,
        indent=4,
        require_default=False,
        set_default_from_json=False
    )
    return code


