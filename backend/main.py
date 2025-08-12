from fastapi import FastAPI
from models import Base
from database import engine
from routes import user_routes
from fastapi.middleware.cors import CORSMiddleware

# Create tables
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management API")

# Allow origins (adjust origins as needed)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    # add your frontend URLs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] to allow all (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],          # allow all methods like GET, POST, OPTIONS etc.
    allow_headers=["*"],          # allow all headers
)

# Register routes
app.include_router(user_routes.router)
