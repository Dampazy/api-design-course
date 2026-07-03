from __future__ import annotations

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.progress import FinalTestProgressOut, ProgressOut
from app.services import progress_service

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("", response_model=ProgressOut)
def get_progress(
    x_session_id: str = Header(...),
    db: Session = Depends(get_db),
) -> ProgressOut:
    return progress_service.get_progress(db, x_session_id)


@router.get("/final-test", response_model=FinalTestProgressOut)
def get_final_test_progress(
    x_session_id: str = Header(...),
    db: Session = Depends(get_db),
) -> FinalTestProgressOut:
    return progress_service.get_final_test_progress(db, x_session_id)
