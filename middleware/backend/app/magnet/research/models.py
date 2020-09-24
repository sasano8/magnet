from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from magnet.database import Base
from . import schemas

# TODO: ツリー構造を実現したい
# https://kite.com/blog/python/sqlalchemy/
class CaseNode(Base): #ノードの情報
    __tablename__ = "case_node"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    is_system = Column(Boolean, default=False, nullable=False) # ルートのみに利用する想定
    description = Column(String(255), nullable=False)


class Target(Base): #ノードの情報
    __tablename__ = "target"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    node_id = Column(Integer, ForeignKey('case_node.id'))

