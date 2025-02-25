import datetime
from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class Locations(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(50))
    location_type = Column(String(50))
    
