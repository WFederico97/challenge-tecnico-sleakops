from fastapi_pagination import add_pagination
from Routes.ProductRoutes import router as product_router
from Routes.LoadAwsDataRoute import router as load_aws_data_router
from Db.db import create_tables
from fastapi import FastAPI

app = FastAPI()
create_tables()

app.include_router(product_router)
app.include_router(load_aws_data_router)

add_pagination(app)