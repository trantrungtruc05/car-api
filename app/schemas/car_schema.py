from typing import Optional
from pydantic import BaseModel, Field


class CarsBase(BaseModel):
    car_id: str = Field(..., min_length=1, max_length=255, description="Mã xe")
    brand: str = Field(..., min_length=1, max_length=255, description="Hãng xe")
    name: str = Field(..., min_length=1, max_length=255, description="Tên xe")
    price: str = Field(..., min_length=1, max_length=255, description="Giá xe")
    location: str = Field(..., min_length=1, max_length=255, description="Vị trí xe")
    status: str = Field(..., min_length=1, max_length=255, description="Trạng thái xe")
    year: str = Field(..., min_length=1, max_length=255, description="Năm xe")
    description: Optional[str] = Field(default="", description="Mô tả xe")
    mileage: Optional[str] = Field(default="", max_length=255, description="Số km xe")
    origin: Optional[str] = Field(default="", max_length=255, description="Xuất xứ xe")
    body_type: Optional[str] = Field(default="", max_length=255, description="Kiểu dáng xe")
    transmission: Optional[str] = Field(default="", max_length=255, description="Hộp số xe")
    engine: Optional[str] = Field(default="", max_length=255, description="Động cơ xe")
    exterior_color: Optional[str] = Field(default="", max_length=255, description="Màu ngoại thất xe")
    interior_color: Optional[str] = Field(default="", max_length=255, description="Màu nội thất xe")
    capacity: Optional[str] = Field(default="", max_length=255, description="Số chỗ ngồi xe")
    number_of_doors: Optional[str] = Field(default="", max_length=255, description="Số cửa xe")
    drive_train: Optional[str] = Field(default="", max_length=255, description="Dẫn động xe")
    seller_name: Optional[str] = Field(default="", max_length=255, description="Tên người bán xe")
    address_seller: Optional[str] = Field(default="", max_length=255, description="Địa chỉ người bán xe")
    phones: Optional[str] = Field(default="", max_length=255, description="Số điện thoại người bán xe")


class CarsCreate(CarsBase):
    pass