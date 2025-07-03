from fastapi import FastAPI
from bosh_sahifa import views as bosh_sahifa_router
from institut import views as institut_router

app = FastAPI()

app.include_router(bosh_sahifa_router.router)
app.include_router(institut_router.router)

@app.get("/")
async def root():
    return {"message": "TMSITI API is running"}
