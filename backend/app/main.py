from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import upload
from app.config.db import db

app = FastAPI()

# Root test
@app.get("/")
def home():
    return {"message": "AutoStylist API running"}

# Routes
app.include_router(upload.router, prefix="/api")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/test-db")
def test_db():
    db.test.insert_one({"status": "connected"})
    return {"message": "MongoDB connected"}