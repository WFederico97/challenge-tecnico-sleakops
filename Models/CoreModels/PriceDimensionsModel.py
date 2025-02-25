import datetime
from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from Db.db import Base

class PriceDimensions(Base):
    __tablename__ = 'price_dimensions'
    price_dimension_id = Column(Integer, primary_key=True, index=True)
    term_id = Column(Integer, ForeignKey('terms.term_id', ondelete="CASCADE"), nullable=False)
    term_type_id = Column(Integer, ForeignKey('term_types.term_type_id'), nullable=False)
    description = Column(String(180))
    unit = Column(String(50))
    price_per_unit = Column(Float)
    currency = Column(String(50))
    applies_to = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(tz=datetime.timezone.utc))