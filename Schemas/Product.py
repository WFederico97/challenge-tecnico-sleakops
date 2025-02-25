from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime

class PriceDimensionRead(BaseModel):
    description: str
    unit: str
    price_per_unit: float
    currency: str
    
    class Config:
        orm_mode = True

class TermRead(BaseModel):
    term_type: str
    purchase_option: Optional[str]
    lease_contract_length: Optional[str]
    effective_date: datetime
    price_dimensions: List[PriceDimensionRead]
    
    @validator('term_type', pre=True)
    def extract_term_type(cls, v):
        if hasattr(v, 'term_type'):
            return v.term_type
        return str(v)
    
    @validator('purchase_option', pre=True)
    def extract_purchase_option(cls, v):
        if hasattr(v, 'purchase_option'):
            return v.purchase_option
        return str(v) if v else None
    
    class Config:
        orm_mode = True

class ProductRead(BaseModel):
    product_id: int
    sku: str
    instance_type: Optional[str]
    vcpu: Optional[int]
    memory: Optional[int]
    database_engine: Optional[str]
    product_family: Optional[str]
    deployment_options: Optional[str]
    terms: List[TermRead] = []

    @validator('deployment_options', pre=True)
    def ensure_deployment_options(cls, v):
        return v or ""
    
    @validator('terms', pre=True)
    def ensure_terms(cls, v):
        return v or []

    class Config:
        orm_mode = True

class TermCreate(BaseModel):
    term_type: str
    purchase_option: Optional[str]
    lease_contract_length: Optional[str]
    price_per_unit: float
    currency: str = "USD"
    unit: str = "Hrs"