from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base schema cho Category
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Tên danh mục")
    link: Optional[str] = Field(None, max_length=500, description="Liên kết danh mục")
    code: str = Field(..., min_length=1, max_length=100, description="Mã danh mục (unique)")

# Schema cho tạo Category mới
class CategoryCreate(CategoryBase):
    pass



# Schema cho response Category
class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


