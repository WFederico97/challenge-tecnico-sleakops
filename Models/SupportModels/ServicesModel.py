import datetime
from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class Services(Base):
    __tablename__ = 'services'
    service_id = Column(Integer, primary_key=True, index=True)
    service_code = Column(String(50))
    service_name = Column(String(50))
    
