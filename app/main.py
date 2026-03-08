from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI(title="Audio to Score API")

app.include_router(upload_router)


@app.get("/")
def root():
    return {"message": "Audio to Score API is running"}