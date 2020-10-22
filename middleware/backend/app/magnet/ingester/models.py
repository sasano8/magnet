from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON, ARRAY, Text
from sqlalchemy.orm import relationship
from magnet.database import Base


class IngesterJobGroup(Base):
    __tablename__ = "ingester_jobgroup"
    id = Column(Integer, primary_key=True)
    is_system = Column(Boolean, nullable=False, default=False)
    description = Column(String(1023), nullable=False, default="")
    target_id = Column(Integer, nullable=True)
    children = relationship("IngesterJob")


class IngesterJob(Base):
    __tablename__ = "ingester_job"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('ingester_jobgroup.id'))
    description = Column(String(1023), nullable=False, default="")
    pipeline_name = Column(String(255), nullable=True)
    crawler_name = Column(String(255), nullable=True)
    keyword = Column(String(255), nullable=True)
    option_keywords = Column(JSON, nullable=False, default=[])
    deps = Column(Integer, nullable=False, default=-1)
    children = relationship("Ingester")


class Ingester(Base):
    __tablename__ = "ingester"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('ingester_job.id'))
    pipeline_name = Column(String(255), nullable=True)
    crawler_name = Column(String(255), nullable=True)
    keyword = Column(String(255), nullable=True)
    option_keywords = Column(JSON, nullable=False, default=[])
    deps = Column(Integer, nullable=False, default=-1)
    referer = Column(String(1023), nullable=True)
    url = Column(String(1023), nullable=True)
    url_cache = Column(String(1023), nullable=True)
    title = Column(String(1023), nullable=True, default="")
    summary = Column(String(1023), nullable=True, default="")
    current_page_num = Column(Integer, nullable=False, default=-1)
    detail = Column(JSON, nullable=False, default={})

