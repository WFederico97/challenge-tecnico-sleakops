import datetime
from typing import List
from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from Db.db import Base
from Models.CoreModels.PriceDimensionsModel import PriceDimensions

class Terms(Base):
    __tablename__ = 'terms'
    term_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    term_type_id = Column(Integer, ForeignKey('term_types.term_type_id'))
    purchase_option_id = Column(Integer, ForeignKey('purchase_options.purchase_option_id'))
    offering_class_id = Column(Integer, ForeignKey('offering_classes.offering_class_id'))
    effective_date = Column(TIMESTAMP)
    term_duration = Column(String(50))
    term_attributes = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(tz=datetime.timezone.utc))

    product = relationship("Product", back_populates="terms")
    term_type_rel = relationship("TermTypes")
    purchase_option_rel = relationship("PurchaseOptions")
    offering_class_rel = relationship("OfferingClasses")