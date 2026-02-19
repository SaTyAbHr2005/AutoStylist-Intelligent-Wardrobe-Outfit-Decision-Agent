from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import upload, recommend
from app.config.db import db
from app.routes import feedback

app = FastAPI()

# Root test
@app.get("/")
def home():
    return {"message": "AutoStylist API running"}


# API Routes
app.include_router(upload.router, prefix="/api")
app.include_router(recommend.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")


# Static files (processed images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# MongoDB test
@app.get("/test-db")
def test_db():
    db.test.insert_one({"status": "connected"})
    return {"message": "MongoDB connected"}
