from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.transcript_service import get_student_transcript, get_all_transcripts

router = APIRouter(prefix="/transcripts", tags=["transcripts"])

# Get all students summary
@router.get("/", summary="Get all students transcript summary")
def fetch_all_transcripts(db: Session = Depends(get_db)):
    return get_all_transcripts(db)

# Get single student transcript with courses
@router.get("/{student_id}", summary="Get a student transcript with course details")
def fetch_transcript(student_id: int, db: Session = Depends(get_db)):
    transcript = get_student_transcript(db, student_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Student transcript not found")
    return transcript
