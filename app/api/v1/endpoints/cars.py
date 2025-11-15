from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.crawler.car_crawler import start_crawl
from pydantic import BaseModel


router = APIRouter()

class InfoCrawlCars(BaseModel):
    start_page: int
    end_page: int

@router.post("/crawl-cars", response_model=dict)
def crawl_and_import_cars(info: InfoCrawlCars, db: Session = Depends(get_db)):
    """Call crawl cars from bonbanh.com"""
    start_crawl(info.start_page, info.end_page)
    return {"status": "success", "message": "Crawl and import completed"}