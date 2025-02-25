from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class TermTypes(Base):
    __tablename__ = 'term_types'
    term_type_id = Column(Integer, primary_key=True, index=True)
    term_type = Column(String(50))
