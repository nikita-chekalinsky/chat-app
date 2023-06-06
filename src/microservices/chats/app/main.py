from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.routers.chats import router as chats_router
from app.services.db_init import on_startup, on_shutdown


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


app.include_router(chats_router,
                   tags=["chats"],
                   prefix="/chats")


app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])
