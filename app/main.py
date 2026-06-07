from fastapi import FastAPI
from app.api.routes import router
from app.api.analysis import router as analysis_router
from app.db.session import engine, Base

app = FastAPI(title="GitHub Engineering Assistant")


@app.on_event("startup")
async def on_startup():
	# Create DB tables if they don't exist (development convenience)
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown():
	await engine.dispose()


app.include_router(router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
