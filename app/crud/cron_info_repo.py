from sqlalchemy.orm import Session
from app.models.cron_info_model import CronInfo
from app.schemas.cron_info_schema import CronInfoCreate
from datetime import datetime

class CronInfoCRUD:

    # update cron info
    def update_cron_info_run_at(self, db: Session, job_name: str, run_at: datetime) -> CronInfo:
        """Cập nhật cron info"""
        db_cron_info = db.query(CronInfo).filter(CronInfo.job_name == job_name).first()
        db_cron_info.run_at = run_at
        db.commit()
        db.refresh(db_cron_info)
        return db_cron_info

    # update cron info run end at
    def update_cron_info_run_end_at(self, db: Session, job_name: str, run_end_at: datetime) -> CronInfo:
        """Cập nhật cron info"""
        db_cron_info = db.query(CronInfo).filter(CronInfo.job_name == job_name).first()
        db_cron_info.run_end_at = run_end_at
        db.commit()
        db.refresh(db_cron_info)
        return db_cron_info

# Tạo instance để sử dụng
cron_info_crud = CronInfoCRUD()