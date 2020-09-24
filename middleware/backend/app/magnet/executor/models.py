from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from magnet.database import Base


class Executor(Base):
    __tablename__ = "executor"
    id = Column(Integer, primary_key=True, index=True)
    is_system = Column(Boolean, nullable=False, default=False)
    # executor_id = Column(String, nullable=False)
    # pipeline_id = Column(Integer, nullable=False)
    name = Column(String, nullable=True, default="")
    description = Column(String, nullable=False, default="")
    executor_name = Column(String, nullable=False, default="")
    pipeline_name = Column(String, nullable=False, default="")


class ExecutorJob(Base):
    __tablename__ = "executor_job"
    id = Column(Integer, primary_key=True, index=True)
    pipeline = Column(String(255), nullable=True)
    crawler_name = Column(String(255), nullable=True)
    keyword = Column(String(255), nullable=True)
    option_keywords = Column(JSON, nullable=False, default=[])
    deps = Column(Integer, nullable=False, default=-1)