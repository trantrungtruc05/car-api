from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class CronInfo(Base):
    __tablename__ = "cron_info"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_name = Column(String(255), nullable=True)
    run_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<CronInfo(id={self.id}, run_at='{self.run_at}')>"