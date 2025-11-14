from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.crawler.car_crawler import start_crawl


router = APIRouter()

@router.post("/crawl-cars", response_model=dict)
def crawl_and_import_cars(db: Session = Depends(get_db)):
    """Call crawl cars from bonbanh.com"""
    start_crawl()
    return {"status": "success", "message": "Crawl and import completed"}