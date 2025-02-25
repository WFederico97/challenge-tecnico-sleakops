from sqlalchemy.orm import Session
from typing import Dict, List,Optional
from Models.CoreModels.ProductsModel import Product
from Models.CoreModels.TermsModel import Terms
from Models.SupportModels.DatabaseEnginesModel import DatabaseEngines
from Models.SupportModels.InstanceTypesModel import InstanceTypes
from Models.SupportModels.PurchaseOptionsModel import PurchaseOptions
from Models.SupportModels.TermTypesModel import TermTypes

class ProductRepository:
    def __init__(self, db:Session):
        self.db = db
    
    def create(self, product:Product):
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_all_products(self, skip:int = 0 , limit:int = 50)->List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def get_by_sku(self, sku:str)->Optional[Product]:
        return self.db.query(Product).filter(Product.sku == sku).first()
    
    def filter_products(self, db_engine: Optional[str] = None,
                        instance_type: Optional[str] = None,
                        location: Optional[str] = None,
                        product_family: Optional[str] = None,
                        term: Optional[str] = None,
                        operation: Optional[str] = None,
                        deployment_option: Optional[str] = None)->List[Product]:
        query = self.db.query(Product)
        if db_engine:
            query = query.filter(Product.db_engine_id == db_engine)
        if instance_type:
            query = query.filter(Product.instance_type_id == instance_type)
        if location:
            query = query.filter(Product.location_id == location)
        if product_family:
            query = query.filter(Product.product_family == product_family)
        if term:
            query = query.filter(Product.term_id == term)
        if operation:
            query = query.filter(Product.operation == operation)
        if deployment_option:
            query = query.filter(Product.deployment_option == deployment_option)
        return query.all()
    
    def search_products(self,
                    database_engine: Optional[str] = None,
                    instance_type: Optional[str] = None, 
                    vcpu: Optional[int] = None,
                    memory: Optional[int] = None) -> List[Dict]:
        query = self.db.query(
            Product,
            DatabaseEngines.engine_name,
            InstanceTypes.instance_type,
            InstanceTypes.vcpu,
            InstanceTypes.memory,
            Terms.term_id,
            Terms.term_duration,
            Terms.effective_date,
            Terms.term_attributes,
            TermTypes.term_type,
            PurchaseOptions.purchase_option
        ).join(
            DatabaseEngines,
            Product.db_engine_id == DatabaseEngines.db_engine_id
        ).join(
            InstanceTypes,
            Product.instance_type_id == InstanceTypes.instance_type_id
        ).outerjoin(
            Terms,
            Product.product_id == Terms.product_id
        ).outerjoin(
            TermTypes,
            Terms.term_type_id == TermTypes.term_type_id
        ).outerjoin(
            PurchaseOptions,
            Terms.purchase_option_id == PurchaseOptions.purchase_option_id
        )
        
        if database_engine:
            query = query.filter(DatabaseEngines.engine_name == database_engine)
        
        if instance_type:
            query = query.filter(InstanceTypes.instance_type == instance_type)
        
        if vcpu:
            query = query.filter(InstanceTypes.vcpu == vcpu)
        
        if memory:
            query = query.filter(InstanceTypes.memory == memory)
        
        results = query.all()
        
        products_map = {}
        for row in results:
            product = row[0]
            if product.product_id not in products_map:
                products_map[product.product_id] = {
                    'product_id': product.product_id,
                    'sku': product.sku,
                    'instance_type': row[2],
                    'vcpu': row[3],
                    'memory': row[4],
                    'database_engine': row[1],
                    'product_family': product.product_family,
                    'deployment_options': product.deployment_options,
                    'terms': []
                }
            
            if row[5]:  # terms
                term = {
                    'term_id': row[5],
                    'term_type': row[9],
                    'purchase_option': row[10],
                    'lease_contract_length': row[6],
                    'effective_date': row[7],
                    'term_attributes': row[8],
                    'price_dimensions': self._get_price_dimensions(row[5])
                }
                
                # unique terms
                if term not in products_map[product.product_id]['terms']:
                    products_map[product.product_id]['terms'].append(term)
        
        return list(products_map.values())
    
    def _get_price_dimensions(self, term_id: int) -> List[Dict]:
        from Models.CoreModels.PriceDimensionsModel import PriceDimensions
        
        price_dimensions = self.db.query(PriceDimensions).filter(
            PriceDimensions.term_id == term_id
        ).all()
        
        return [{
            'description': pd.description,
            'unit': pd.unit,
            'price_per_unit': pd.price_per_unit,
            'currency': pd.currency
        } for pd in price_dimensions]