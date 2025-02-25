# Services/DataLoaderService.py
import json
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from Models.CoreModels.ProductsModel import Product
from Models.CoreModels.TermsModel import Terms
from Models.CoreModels.PriceDimensionsModel import PriceDimensions
from Models.SupportModels.ServicesModel import Services
from Models.SupportModels.LocationsModel import Locations
from Models.SupportModels.InstanceTypesModel import InstanceTypes
from Models.SupportModels.DatabaseEnginesModel import DatabaseEngines
from Models.SupportModels.LicenseModels import LicenseModels
from Models.SupportModels.TermTypesModel import TermTypes
from Models.SupportModels.PurchaseOptionsModel import PurchaseOptions
from Models.SupportModels.OfferingClasses import OfferingClasses

class DataLoaderService:
    def __init__(self, db: Session):
        self.db = db

    def LoadDataFromAws(self, json_file_path: str) -> None:
        try:
            with open(json_file_path, 'r') as file:
                aws_data = json.load(file)

            for sku, product_data in aws_data['products'].items():
                try:
                    attributes = product_data.get('attributes', {})

                    product = Product(
                        service_id=self._get_or_create_service(
                            attributes.get('servicecode', 'N/A'),
                            attributes.get('servicename', 'N/A')
                        ).service_id,
                        location_id=self._get_or_create_location(
                            attributes.get('location', 'N/A'),
                            attributes.get('locationType', 'N/A')
                        ).location_id,
                        instance_type_id=self._get_or_create_instance_type(
                            attributes.get('instanceType', 'N/A'),
                            int(attributes.get('vcpu', 0)),
                            attributes.get('memory', '0 GiB').split()[0],
                            attributes.get('usagetype', 'N/A')
                        ).instance_type_id,
                        db_engine_id=self._get_or_create_database_engine(
                            attributes.get('databaseEngine', 'N/A')
                        ).db_engine_id,
                        license_model_id=self._get_or_create_license_model(
                            attributes.get('licenseModel', 'N/A')
                        ).license_model_id,
                        sku=product_data['sku'],
                        product_family=product_data.get('productFamily', 'N/A'),
                        operation=attributes.get('operation', 'N/A'),
                        deployment_options=attributes.get('deploymentOption', 'N/A')
                    )
                    self.db.add(product)
                    self.db.flush()
                    if sku in aws_data['terms'].get('OnDemand', {}):
                        self._process_terms(aws_data['terms']['OnDemand'][sku], product.product_id, 'OnDemand')
                    if sku in aws_data['terms'].get('Reserved', {}):
                        self._process_terms(aws_data['terms']['Reserved'][sku], product.product_id, 'Reserved')

                except Exception as e:
                    print(f"Error processing product {sku}: {str(e)}")
                    continue

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error loading AWS data: {str(e)}")

    def _process_terms(self, term_data: Dict, product_id: int, term_type: str) -> None:
        for term_id, term_info in term_data.items():
            term_attributes = term_info.get('termAttributes', {})
            
            term = Terms(
                product_id=product_id,
                term_type_id=self._get_or_create_term_type(term_type).term_type_id,
                purchase_option_id=self._get_or_create_purchase_option(
                    term_attributes.get('PurchaseOption', 'N/A')
                ).purchase_option_id,
                offering_class_id=self._get_or_create_offering_class(
                    term_attributes.get('OfferingClass', 'standard')
                ).offering_class_id,
                effective_date=datetime.fromisoformat(term_info['effectiveDate'].replace('Z', '+00:00')),
                term_duration=term_attributes.get('LeaseContractLength', 'N/A'),
                term_attributes=term_attributes
            )
            self.db.add(term)
            self.db.flush()

            for price_dimension in term_info.get('priceDimensions', {}).values():
                price_dimension_obj = PriceDimensions(
                    term_id=term.term_id,
                    term_type_id=term.term_type_id,
                    description=price_dimension.get('description', ''),
                    unit=price_dimension.get('unit', ''),
                    price_per_unit=float(price_dimension.get('pricePerUnit', {}).get('USD', 0)),
                    currency='USD',
                    applies_to=price_dimension.get('appliesTo', [])
                )
                self.db.add(price_dimension_obj)

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

    def _get_or_create_offering_class(self, offering_class: str) -> OfferingClasses:
        offering_class_obj = self.db.query(OfferingClasses).filter_by(offering_class=offering_class).first()
        if not offering_class_obj:
            offering_class_obj = OfferingClasses(offering_class=offering_class)
            self.db.add(offering_class_obj)
            self.db.flush()
        return offering_class_obj

    def _get_or_create_service(self, service_code: str, service_name: str) -> Services:
        service = self.db.query(Services).filter_by(service_code=service_code).first()
        if not service:
            service = Services(
                service_code=service_code,
                service_name=service_name
            )
            self.db.add(service)
            self.db.flush()
        return service

    def _get_or_create_location(self, location_name: str, location_type: str) -> Locations:
        location = self.db.query(Locations).filter_by(location_name=location_name).first()
        if not location:
            location = Locations(
                location_name=location_name,
                location_type=location_type
            )
            self.db.add(location)
            self.db.flush()
        return location

    def _get_or_create_instance_type(self, instance_type: str, vcpu: int, memory: str, usage_type: str) -> InstanceTypes:
        instance = self.db.query(InstanceTypes).filter_by(instance_type=instance_type).first()
        if not instance:
            instance = InstanceTypes(
                instance_type=instance_type,
                vcpu=vcpu,
                memory=int(float(memory)),
                usage_type=usage_type
            )
            self.db.add(instance)
            self.db.flush()
        return instance

    def _get_or_create_database_engine(self, engine_name: str) -> DatabaseEngines:
        engine = self.db.query(DatabaseEngines).filter_by(engine_name=engine_name).first()
        if not engine:
            engine = DatabaseEngines(
                engine_name=engine_name
            )
            self.db.add(engine)
            self.db.flush()
        return engine

    def _get_or_create_license_model(self, license_name: str) -> LicenseModels:
        license_model = self.db.query(LicenseModels).filter_by(license_name=license_name).first()
        if not license_model:
            license_model = LicenseModels(
                license_name=license_name
            )
            self.db.add(license_model)
            self.db.flush()
        return license_model