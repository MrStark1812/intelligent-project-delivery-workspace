from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import Project

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Project Delivery Workspace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "IPDW backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}