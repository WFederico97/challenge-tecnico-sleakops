from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class LicenseModels(Base):
    __tablename__ = 'license_models'
    license_model_id = Column(Integer, primary_key=True, index=True)
    license_name = Column(String(50))
    
