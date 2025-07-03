from fastapi import FastAPI
from core.database import Base, engine
from auth.views import router as auth_router
from bosh_sahifa.views import router as bosh_router
from institut.views import router as institut_router

app = FastAPI(title="TMSITI API")

# Routers
app.include_router(auth_router)
app.include_router(bosh_router)
app.include_router(institut_router)

@app.get("/")
async def root():
    return {"message": "TMSITI API is running"}

# Create tables on start
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
