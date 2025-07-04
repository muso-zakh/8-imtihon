from fastapi import FastAPI
from core.database import Base, engine
from auth.views import router as auth_router
from bosh_sahifa.views import router as bosh_router
from institut.views import router as institut_router
from institut.views import router2 as rahbariyat_router
from institut.views import router3 as tuzilma_router
from institut.views import router4 as tarkibiy_router
from menyu.views import router5 as menyu_router
from hujjatlar.views import router6 as hujjatlar_router
from hujjatlar.views import router7 as standardlar_router


app = FastAPI(title="TMSITI API")

# Routers
app.include_router(auth_router)
app.include_router(menyu_router)
app.include_router(bosh_router)
app.include_router(institut_router)
app.include_router(rahbariyat_router)
app.include_router(tuzilma_router)
app.include_router(tarkibiy_router)
app.include_router(hujjatlar_router)
app.include_router(standardlar_router)

@app.get("/")
async def root():
    return {"message": "TMSITI API is running"}

# Create tables on start
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
