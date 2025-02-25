from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class PurchaseOptions(Base):
    __tablename__ = 'purchase_options'
    purchase_option_id = Column(Integer, primary_key=True, index=True)
    purchase_option = Column(String(50))
    
