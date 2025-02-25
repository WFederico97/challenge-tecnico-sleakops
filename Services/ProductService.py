from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime
from Models.CoreModels.ProductsModel import Product
from Models.CoreModels.TermsModel import Terms
from Models.CoreModels.PriceDimensionsModel import PriceDimensions
from Models.SupportModels.PurchaseOptionsModel import PurchaseOptions
from Models.SupportModels.TermTypesModel import TermTypes
from Repositories.ProductRepository import ProductRepository
from Schemas.Product import TermCreate

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
    
    def search_products(self, 
                    database_engine: Optional[str] = None,
                    instance_type: Optional[str] = None,
                    vcpu: Optional[int] = None,
                    memory: Optional[int] = None) -> List[Dict]:
        return self.product_repository.search_products(
            database_engine=database_engine,
            instance_type=instance_type,
            vcpu=vcpu,
            memory=memory
        )
    
    def add_term(self, sku: str, term_data: TermCreate):
        product = self.product_repository.get_by_sku(sku)
        if not product:
            raise Exception(f"Product with SKU {sku} not found")
            
        term_type_obj = self._get_or_create_term_type(term_data.term_type)
        purchase_option_obj = self._get_or_create_purchase_option(term_data.purchase_option)

        term = Terms(
            product_id=product.product_id,
            term_type_id=term_type_obj.term_type_id,
            purchase_option_id=purchase_option_obj.purchase_option_id,
            term_duration=term_data.lease_contract_length,
            effective_date=datetime.utcnow(),
            term_attributes={}
        )
        self.db.add(term)
        self.db.flush()
        
        price_dimension = PriceDimensions(
            term_id=term.term_id,
            term_type_id=term_type_obj.term_type_id,
            description=f"{term_data.price_per_unit} per {term_data.unit}",
            unit=term_data.unit,
            price_per_unit=term_data.price_per_unit,
            currency=term_data.currency
        )
        self.db.add(price_dimension)
        self.db.commit()
        
        return term

    def update_term(self, sku: str, term_id: int, term_data: TermCreate):
        product = self.product_repository.get_by_sku(sku)
        if not product:
            raise Exception(f"Product with SKU {sku} not found")
            
        term = self.db.query(Terms).filter(
            Terms.term_id == term_id,
            Terms.product_id == product.product_id
        ).first()
        
        if not term:
            raise Exception(f"Term {term_id} not found for SKU {sku}")
            
        term.term_type = term_data.term_type
        term.purchase_option = term_data.purchase_option
        term.term_duration = term_data.lease_contract_length
        
        price_dimension = self.db.query(PriceDimensions).filter(
            PriceDimensions.term_id == term_id
        ).first()
        
        if price_dimension:
            price_dimension.description = f"{term_data.price_per_unit} per {term_data.unit}"
            price_dimension.unit = term_data.unit
            price_dimension.price_per_unit = term_data.price_per_unit
            price_dimension.currency = term_data.currency
            
        self.db.commit()
        return term

    def delete_term(self, sku: str, term_id: int):
        product = self.product_repository.get_by_sku(sku)
        if not product:
            raise Exception(f"Product with SKU {sku} not found")
            
        self.db.query(PriceDimensions).filter(
            PriceDimensions.term_id == term_id
        ).delete(synchronize_session=False)
        
        term = self.db.query(Terms).filter(
            Terms.term_id == term_id,
            Terms.product_id == product.product_id
        ).first()
        
        if not term:
            raise Exception(f"Term {term_id} not found for SKU {sku}")
            
        self.db.delete(term)
        
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error deleting term: {str(e)}")
        
    def _get_or_create_term_type(self, term_type: str) -> TermTypes:
        term_type_obj = self.db.query(TermTypes).filter_by(term_type=term_type).first()
        if not term_type_obj:
            term_type_obj = TermTypes(term_type=term_type)
            self.db.add(term_type_obj)
            self.db.flush()
        return term_type_obj

    def _get_or_create_purchase_option(self, purchase_option: str) -> PurchaseOptions:
        purchase_option_obj = self.db.query(PurchaseOptions).filter_by(purchase_option=purchase_option).first()
        if not purchase_option_obj:
            purchase_option_obj = PurchaseOptions(purchase_option=purchase_option)
            self.db.add(purchase_option_obj)
            self.db.flush()
        return purchase_option_obj