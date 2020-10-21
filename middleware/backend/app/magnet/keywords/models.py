from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from magnet.database import Base

class Keywords(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    category_name = Column(String, unique=True, index=True)
    tag  = Column(String, index=True)
    keywords: Column(JSON, nullable=False, default=[])
    max_size = Column(Integer)


