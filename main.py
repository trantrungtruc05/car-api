from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.database import engine
from app.core.config import settings
from app.models import Category
from app.models import Cars
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from contextlib import asynccontextmanager
from app.services.crawler.car_crawler import start_crawl

logging.basicConfig(level=logging.INFO)

# Tạo bảng trong database
Category.metadata.create_all(bind=engine)
Cars.metadata.create_all(bind=engine)

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Quản lý vòng đời của ứng dụng.
    Code trước yield chạy khi startup, code sau yield chạy khi shutdown.
    """
    # Startup
    logging.info("🚀 Khởi động Scheduler...")
    
    # Thêm tác vụ: chạy mỗi 5 giây
    scheduler.add_job(
        start_crawl(), 
        'interval', 
        hours=6, 
        id='crawl_6_hour_job',
        replace_existing=True,
        max_instances=1
    )
    
    scheduler.start()
    logging.info("✅ Scheduler đã khởi động!")
    
    yield
    
    # Shutdown
    logging.info("🛑 Dừng Scheduler...")
    scheduler.shutdown()
    logging.info("✅ Scheduler đã dừng!")

app = FastAPI(
    title=settings.app_name,
    description="API cho quản lý danh mục xe hơi",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.api_v1_prefix)

@app.get("/")
def read_root():
    return {
        "message": "Chào mừng đến với Car API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
