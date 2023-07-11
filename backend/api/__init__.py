from api.routes import router as cases_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(cases_router, prefix="/cases", tags=["cases"])


@app.get("/health-check")
async def health_check():
    return {"msg": "API is healthy"}
