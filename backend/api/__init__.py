from fastapi import FastAPI

from backend.api.routes import router as cases_router

app = FastAPI()


app.include_router(cases_router, prefix="/cases", tags=["cases"])


@app.get("/health-check")
async def health_check():
    return {"msg": "API is healthy"}
