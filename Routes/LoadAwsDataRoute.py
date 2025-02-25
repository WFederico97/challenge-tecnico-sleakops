from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from Db.db import get_db
from Services.DataLoaderService import DataLoaderService

router = APIRouter(prefix="/loadData", tags=["AWS Data"])
@router.post("/load-aws-data", status_code=201, summary="Load AWS pricing data")
def load_aws_data(db: Session = Depends(get_db)):
    try:
        data_loader = DataLoaderService(db)
        data_loader.LoadDataFromAws("awsPrices.json")
        return {"message": "Data loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))