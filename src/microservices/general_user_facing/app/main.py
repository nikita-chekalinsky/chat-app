from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.services.db_init import on_startup, on_shutdown
from .routers.user_info import router as user_info_router

app = FastAPI()
security = HTTPBearer()


@app.get('/')
async def root():
    return {'message': 'Go to /docs to see the documentation'}


@app.get('/health')
async def health():
    return {'message': 'ok'}


@app.on_event("startup")
async def startup():
    await on_startup()


@app.on_event("shutdown")
async def shutdown():
    await on_shutdown()

app.include_router(user_info_router, tags=[
                   "users-info"], prefix="/users-info")


app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])
