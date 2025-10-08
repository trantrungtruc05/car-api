from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict
from app.models.category import Category
from app.schemas.category import CategoryCreate

class CategoryCRUD:
    def create_category(self, db: Session, category: CategoryCreate) -> Category:
        """Tạo category mới"""
        db_category = Category(
            name=category.name,
            link=category.link,
            code=category.code
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    

    
    def get_category_by_code(self, db: Session, code: str) -> Optional[Category]:
        """Lấy category theo code"""
        return db.query(Category).filter(Category.code == code).first()
    
    def get_categories(
        self, 
        db: Session, 
        search: Optional[str] = None
    ) -> List[Category]:
        """Lấy danh sách categories với tìm kiếm"""
        query = db.query(Category)
        
        # Tìm kiếm theo name hoặc code
        if search:
            query = query.filter(
                (Category.name.ilike(f"%{search}%")) | 
                (Category.code.ilike(f"%{search}%"))
            )
        
        # Lấy tất cả data không phân trang
        categories = query.order_by(Category.created_at.desc()).all()
        
        return categories
    

    


    def bulk_create_categories(self, db: Session, categories_data: List[Dict[str, str]]) -> List[Category]:
        """Tạo nhiều categories cùng lúc từ dữ liệu crawl"""
        created_categories = []
        
        for category_data in categories_data:
            # Kiểm tra xem category đã tồn tại chưa (theo code)
            existing = self.get_category_by_code(db, category_data.get('code', ''))
            
            if not existing:
                # Tạo category mới
                db_category = Category(
                    name=category_data.get('name', ''),
                    link=category_data.get('link', ''),
                    code=category_data.get('code', '')
                )
                db.add(db_category)
                created_categories.append(db_category)
            else:
                print(f"Category với code '{category_data.get('code')}' đã tồn tại, bỏ qua...")
        
        # Commit tất cả cùng lúc
        if created_categories:
            db.commit()
            # Refresh tất cả objects
            for category in created_categories:
                db.refresh(category)
        
        return created_categories

# Tạo instance để sử dụng
category_crud = CategoryCRUD()
