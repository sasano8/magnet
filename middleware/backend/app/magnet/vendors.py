from fastapi import APIRouter
from sqlalchemy.orm import Session
from libs.fastapi import GenericRepository, TemplateView, build_exception
from libs.linq import Linq, MiniDB
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from libs.pydantic import fastapi_funnel, funnel
