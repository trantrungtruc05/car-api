from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.schemas import Category
from app.crud import category_crud
from app.services.crawler import category_crawler

router = APIRouter()



@router.post("/crawl-and-import", response_model=dict)
def crawl_and_import_categories(
    source: str = Query("sample", description="Nguồn crawl: 'sample', 'otosaigon', hoặc URL cụ thể"),
    db: Session = Depends(get_db)
):
    """Crawl dữ liệu từ web và import vào database"""
    try:
        # Lấy dữ liệu từ crawler
        if source == "sample":
            categories_data = category_crawler.crawl_categories_from_sample_site()
        elif source == "otosaigon":
            categories_data = category_crawler.crawl_categories_from_otosaigon()
        elif source.startswith("http"):
            # Nếu là URL, crawl từ URL đó
            categories_data = category_crawler.crawl_categories_from_real_site(source)
        else:
            raise HTTPException(
                status_code=400,
                detail="Nguồn không hợp lệ. Sử dụng: 'sample', 'otosaigon', hoặc URL cụ thể"
            )
        
        if not categories_data:
            return {
                "message": "Không tìm thấy dữ liệu để import",
                "source": source,
                "imported_count": 0,
                "categories": []
            }
        
        # Import vào database
        created_categories = category_crud.bulk_create_categories(db=db, categories_data=categories_data)
        
        return {
            "message": f"Đã crawl và import thành công từ {source}",
            "source": source,
            "total_found": len(categories_data),
            "imported_count": len(created_categories),
            "skipped_count": len(categories_data) - len(created_categories),
            "categories": [
                {
                    "id": cat.id,
                    "name": cat.name,
                    "code": cat.code,
                    "link": cat.link
                } for cat in created_categories
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi crawl và import: {str(e)}"
        )

@router.post("/crawl-multiple", response_model=dict)
def crawl_from_multiple_sources(
    urls: List[str] = Query(..., description="Danh sách các URL để crawl"),
    db: Session = Depends(get_db)
):
    """Crawl từ nhiều trang web cùng lúc"""
    try:
        # Crawl từ nhiều URL
        all_categories_data = category_crawler.crawl_categories_from_multiple_pages(urls)
        
        if not all_categories_data:
            return {
                "message": "Không tìm thấy dữ liệu từ các URL",
                "sources": urls,
                "imported_count": 0
            }
        
        # Import vào database
        created_categories = category_crud.bulk_create_categories(db=db, categories_data=all_categories_data)
        
        return {
            "message": f"Đã crawl từ {len(urls)} trang web",
            "sources": urls,
            "total_found": len(all_categories_data),
            "imported_count": len(created_categories),
            "skipped_count": len(all_categories_data) - len(created_categories),
            "categories": [
                {
                    "id": cat.id,
                    "name": cat.name,
                    "code": cat.code,
                    "link": cat.link
                } for cat in created_categories
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi crawl từ nhiều nguồn: {str(e)}"
        )

@router.get("/", response_model=list[Category])
def get_categories(
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên hoặc code"),
    db: Session = Depends(get_db)
):
    """Lấy danh sách categories với tìm kiếm"""
    categories = category_crud.get_categories(
        db=db, search=search
    )
    
    return categories







@router.get("/code/{code}", response_model=Category)
def get_category_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Lấy category theo code"""
    category = category_crud.get_category_by_code(db=db, code=code)
    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Category với code '{code}' không tồn tại"
        )
    return category

@router.get("/crawl-preview")
def preview_crawl_data(
    source: str = Query("sample", description="Nguồn crawl: 'sample', 'otosaigon', hoặc URL cụ thể")
):
    """Xem trước dữ liệu sẽ được crawl mà không import vào DB"""
    try:
        if source == "sample":
            categories_data = category_crawler.crawl_categories_from_sample_site()
        elif source == "otosaigon":
            categories_data = category_crawler.crawl_categories_from_otosaigon()
        elif source.startswith("http"):
            categories_data = category_crawler.crawl_categories_from_real_site(source)
        else:
            raise HTTPException(
                status_code=400,
                detail="Nguồn không hợp lệ. Sử dụng: 'sample', 'otosaigon', hoặc URL cụ thể"
            )
        
        return {
            "source": source,
            "total_categories": len(categories_data),
            "categories": categories_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi preview crawl: {str(e)}"
        )
