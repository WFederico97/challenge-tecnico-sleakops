from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class DatabaseEngines(Base):
    __tablename__ = 'database_engines'
    db_engine_id = Column(Integer, primary_key=True, index=True)
    engine_name = Column(String(50))
    
