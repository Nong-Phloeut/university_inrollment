from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers.dashboard_controller import get_dashboard_data_controller
from schemas.dashboard_schema import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    return get_dashboard_data_controller(db)
