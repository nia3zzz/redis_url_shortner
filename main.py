from fastapi import FastAPI
from routes.shortner_routes import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root_controller():
    return {"message": "APIs are running successfully."}
