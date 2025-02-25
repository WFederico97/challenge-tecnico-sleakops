

CREATE TABLE Database_Engines (
  db_engine_id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  engine_name       varchar(80) NOT NULL
);

CREATE TABLE Instance_Types (
  instance_type_id  int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  instance_type     varchar(80) NOT NULL,
  vcpu              int,
  memory            varchar(80),
  usage_type        varchar(80)
);

CREATE TABLE Locations (
  location_id       int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  location_name     varchar(80) NOT NULL,
  location_type     varchar(80)
);

CREATE TABLE Services (
  service_id        int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  service_code      varchar(80) NOT NULL,
  service_name      varchar(80)
);

CREATE TABLE Offering_Classes (
  offering_class_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  offering_class    varchar(80) NOT NULL
);

CREATE TABLE Purchase_Options (
  purchase_option_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  purchase_option    varchar(80) NOT NULL
);

CREATE TABLE Term_Types (
  term_type_id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  term_type         varchar(80) NOT NULL
);

CREATE TABLE License_Models (
  license_model_id  int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  license_name      varchar(80) NOT NULL
);


CREATE TABLE Products (
  product_id          int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku                 varchar(25) NOT NULL,
  service_id          int,
  location_id         int,
  instance_type_id    int,
  db_engine_id        int,
  license_model_id    int,
  product_family      varchar(150),
  operation           varchar(120),
  deployment_options  varchar(120),
  created_at          timestamp DEFAULT now(),
  updated_at          timestamp DEFAULT now(),
  
  CONSTRAINT fk_products_services
    FOREIGN KEY (service_id)
    REFERENCES Services (service_id),
  
  CONSTRAINT fk_products_locations
    FOREIGN KEY (location_id)
    REFERENCES Locations (location_id),
  
  CONSTRAINT fk_products_instance_types
    FOREIGN KEY (instance_type_id)
    REFERENCES Instance_Types (instance_type_id),
  
  CONSTRAINT fk_products_database_engines
    FOREIGN KEY (db_engine_id)
    REFERENCES Database_Engines (db_engine_id),
  
  CONSTRAINT fk_products_license_models
    FOREIGN KEY (license_model_id)
    REFERENCES License_Models (license_model_id)
);



CREATE TABLE Terms (
  term_id           int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_id        int NOT NULL,
  term_type_id      int NOT NULL,
  purchase_option_id int,
  offering_class_id  int,
  effective_date    timestamp,
  term_duration     varchar(120),
  term_attributes   jsonb,
  created_at        timestamp DEFAULT now(),
  updated_at        timestamp DEFAULT now(),
  
  CONSTRAINT fk_terms_products
    FOREIGN KEY (product_id)
    REFERENCES Products (product_id),
  
  CONSTRAINT fk_terms_term_types
    FOREIGN KEY (term_type_id)
    REFERENCES Term_Types (term_type_id),
  
  CONSTRAINT fk_terms_purchase_options
    FOREIGN KEY (purchase_option_id)
    REFERENCES Purchase_Options (purchase_option_id),
  
  CONSTRAINT fk_terms_offering_classes
    FOREIGN KEY (offering_class_id)
    REFERENCES Offering_Classes (offering_class_id)
);



CREATE TABLE Price_Dimensions (
  price_dimension_id  int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  term_id             int NOT NULL,
  term_type_id        int NOT NULL,
  description         varchar(180),
  unit                varchar(50),
  price_per_unit      numeric,
  currency            varchar(120),
  applies_to          jsonb,
  created_at          timestamp DEFAULT now(),
  updated_at          timestamp DEFAULT now(),
  
  CONSTRAINT fk_price_dimensions_terms
    FOREIGN KEY (term_id)
    REFERENCES Terms (term_id),
  
  CONSTRAINT fk_price_dimensions_term_types
    FOREIGN KEY (term_type_id)
    REFERENCES Term_Types (term_type_id)
);