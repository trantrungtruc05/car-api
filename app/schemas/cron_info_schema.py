from pydantic import BaseModel, Field
from datetime import datetime

# Base schema cho CronInfo
class CronInfoBase(BaseModel):
    run_at: datetime = Field(..., description="Thời gian chạy")
    job_name: str = Field(..., description="Tên job")

# Schema cho tạo CronInfo mới
class CronInfoCreate(CronInfoBase):
    pass