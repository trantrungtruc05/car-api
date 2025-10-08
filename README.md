# Car API - FastAPI CRUD Application

Ứng dụng FastAPI với CRUD operations cho bảng Category sử dụng SQLAlchemy ORM, được tổ chức theo chuẩn FastAPI best practices.

## Tính năng

- ✅ Thêm, sửa, xóa, xem danh mục (CRUD)
- ✅ Tìm kiếm theo tên hoặc code
- ✅ Phân trang
- ✅ Validation dữ liệu với Pydantic
- ✅ Auto-generated API documentation
- ✅ SQLAlchemy ORM
- ✅ PostgreSQL/SQLite support
- ✅ Cấu trúc dự án theo best practices
- ✅ Configuration management với Pydantic Settings

## Cấu trúc Database

Bảng `categories` có các cột:
- `id`: Integer, Primary Key, Auto-increment
- `name`: String(255), Not null
- `link`: String(500), Nullable
- `code`: String(100), Unique, Not null
- `created_at`: DateTime, Auto-generated
- `updated_at`: DateTime, Auto-updated

## Cài đặt

1. **Cài đặt dependencies:**
```bash
pip install -r requirement.txt
```

2. **Cấu hình database:**
```bash
cp env_example.txt .env
```
Chỉnh sửa file `.env` với thông tin database của bạn.

3. **Chạy ứng dụng:**
```bash
python main.py
```

Hoặc sử dụng uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Categories
- `POST /api/v1/categories/` - Tạo category mới
- `GET /api/v1/categories/` - Lấy danh sách categories (có phân trang, tìm kiếm)
- `GET /api/v1/categories/{id}` - Lấy category theo ID
- `PUT /api/v1/categories/{id}` - Cập nhật category
- `DELETE /api/v1/categories/{id}` - Xóa category
- `GET /api/v1/categories/code/{code}` - Lấy category theo code

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Ví dụ sử dụng

### Tạo category mới
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Xe sedan",
    "link": "https://example.com/sedan",
    "code": "SEDAN"
  }'
```

### Lấy danh sách categories
```bash
curl "http://localhost:8000/api/v1/categories/?skip=0&limit=10&search=sedan"
```

### Cập nhật category
```bash
curl -X PUT "http://localhost:8000/api/v1/categories/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Xe sedan cao cấp"
  }'
```

### Xóa category
```bash
curl -X DELETE "http://localhost:8000/api/v1/categories/1"
```

## Cấu trúc project (Tối ưu hóa)

```
car_api/
├── main.py                    # Entry point
├── requirement.txt            # Dependencies
├── env_example.txt           # Environment example
├── README.md                 # Documentation
└── app/                      # Main application package
    ├── __init__.py
    ├── core/                 # Core functionality
    │   ├── __init__.py
    │   ├── config.py         # Settings & configuration
    │   └── database.py       # Database setup
    ├── models/               # SQLAlchemy models
    │   ├── __init__.py
    │   └── category.py       # Category model
    ├── schemas/              # Pydantic schemas
    │   ├── __init__.py
    │   └── category.py       # Category schemas
    ├── crud/                 # CRUD operations
    │   ├── __init__.py
    │   └── category.py       # Category CRUD
    └── api/                  # API routes
        ├── __init__.py
        └── v1/               # API version 1
            ├── __init__.py
            ├── api.py        # API router
            └── endpoints/    # Individual endpoints
                ├── __init__.py
                └── categories.py
```

## Lợi ích của cấu trúc mới

### 🎯 **Tổ chức tốt hơn:**
- **Separation of concerns**: Mỗi module có trách nhiệm riêng
- **Scalability**: Dễ dàng thêm models, endpoints mới
- **Maintainability**: Code dễ maintain và debug

### 📁 **Cấu trúc rõ ràng:**
- `app/core/`: Configuration và database setup
- `app/models/`: SQLAlchemy models
- `app/schemas/`: Pydantic schemas cho validation
- `app/crud/`: Business logic operations
- `app/api/`: API routes và endpoints

### ⚙️ **Configuration Management:**
- Sử dụng Pydantic Settings cho type-safe config
- Environment variables với default values
- Centralized configuration

### 🔄 **Versioning:**
- API versioning với `/api/v1/`
- Dễ dàng thêm v2, v3 trong tương lai

## Database Support

### PostgreSQL (Khuyến nghị)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/car_api_db
```

### SQLite (Development)
```env
DATABASE_URL=sqlite:///./car_api.db
```

## Tính năng nâng cao

- **Tìm kiếm**: Tìm theo tên hoặc code
- **Phân trang**: Sử dụng skip và limit
- **Validation**: Kiểm tra unique code
- **Error handling**: HTTP status codes phù hợp
- **Auto timestamps**: Tự động cập nhật created_at và updated_at
- **Type hints**: Full type annotations
- **Configuration**: Environment-based settings