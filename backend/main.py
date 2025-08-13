from fastapi import FastAPI
from models import Base
from database import engine
from routes import user_routes
from routes import dashboard_routes
from routes import student_routes
from routes import grade_routes
from routes import course_routes
from routes import course_enrollments_routes
from routes import transcript_routes
from fastapi.middleware.cors import CORSMiddleware

# Create tables
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management API")

# Allow origins (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(student_routes.router)
app.include_router(grade_routes.router)
app.include_router(course_routes.router)
app.include_router(course_enrollments_routes.router)
app.include_router(transcript_routes.router)
