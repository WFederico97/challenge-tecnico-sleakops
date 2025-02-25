import datetime
from typing import List
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.service_id'), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=False)
    instance_type_id = Column(Integer, ForeignKey('instance_types.instance_type_id'), nullable=False)
    db_engine_id = Column(Integer, ForeignKey('database_engines.db_engine_id'), nullable=False)
    license_model_id = Column(Integer, ForeignKey('license_models.license_model_id'), nullable=False)
    sku = Column(String(50))
    product_family = Column(String(150))
    operation = Column(String(120))
    deployment_options = Column(String(120))
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(tz=datetime.timezone.utc))
    
    database_engines = relationship("DatabaseEngines")
    instance_types = relationship("InstanceTypes")
    terms = relationship("Terms", back_populates="product")
    services = relationship("Services")
    locations = relationship("Locations")
    license_models = relationship("LicenseModels")

