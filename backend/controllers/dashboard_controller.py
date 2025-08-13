from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from services.dashboard_service import get_dashboard_data_service
from schemas.dashboard_schema import DashboardResponse

def get_dashboard_data_controller(db: Session = Depends(get_db)) -> DashboardResponse:
    data = get_dashboard_data_service(db)
    return DashboardResponse(**data)
