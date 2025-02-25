from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class OfferingClasses(Base):
    __tablename__ = 'offering_classes'
    offering_class_id = Column(Integer, primary_key=True, index=True)
    offering_class = Column(String(50))
    
