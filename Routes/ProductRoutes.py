from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from Db.db import get_db
from Services.ProductService import ProductService
from Schemas.Product import ProductRead, TermCreate

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/search", response_model=List[Dict])
def search_products(
    database_engine: Optional[str] = None,
    instance_type: Optional[str] = None,
    vcpu: Optional[int] = None,
    memory: Optional[int] = None,
    db: Session = Depends(get_db)
):
    product_service = ProductService(db)
    try:
        products = product_service.search_products(
            database_engine=database_engine,
            instance_type=instance_type,
            vcpu=vcpu,
            memory=memory
        )
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{sku}/terms")
def add_term(sku: str, term: TermCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    try:
        return product_service.add_term(sku, term)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{sku}/terms/{term_id}")
def update_term(sku: str, term_id: int, term: TermCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    try:
        return product_service.update_term(sku, term_id, term)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{sku}/terms/{term_id}")
def delete_term(sku: str, term_id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    try:
        product_service.delete_term(sku, term_id)
        return {"message": "Term deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))