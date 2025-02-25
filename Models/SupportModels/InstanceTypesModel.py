from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class InstanceTypes(Base):
    __tablename__ = 'instance_types'
    instance_type_id = Column(Integer, primary_key=True, index=True)
    instance_type = Column(String(50))
    vcpu = Column(Integer)
    memory = Column(Integer)
    usage_type = Column(String(50))
    
