from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.crawler.category_crawler import start_crawl


router = APIRouter()

@router.post("/crawl-and-import", response_model=dict)
def crawl_and_import_categories(db: Session = Depends(get_db)):
    """Call crawl categories from bonbanh.com"""
    start_crawl()
    return {"status": "success", "message": "Crawl and import completed"}