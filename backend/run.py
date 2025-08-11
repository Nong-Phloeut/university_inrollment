from fastapi import FastAPI
from models import Base
from database import engine
from routes import user_routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management API")

# Register routes
app.include_router(user_routes.router)
