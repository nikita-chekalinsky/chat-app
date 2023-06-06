from fastapi import APIRouter, Request
from libs.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    UserAddChats,
)
from app.services.user_repository import UserRepository


router = APIRouter()
user_repository = UserRepository()


@router.get('/{user_id}', responses={
    200: {"model": User},
})
async def get_user_info(request: Request,
                        user_id: str) -> User:
    return await user_repository.get_user(request, user_id)


@router.post('/', responses={
    201: {"model": User},
})
async def create_user(request: Request,
                      user: UserCreate) -> User:
    return await user_repository.create_user(user)


@router.put('/', responses={
    201: {"model": User},
})
async def update_user(request: Request,
                      user: UserUpdate) -> User:
    return await user_repository.update_user(user)


@router.post('/add_chat', responses={
    201: {"model": User},
})
async def add_chat(request: Request,
                   user_chats: UserAddChats) -> User:
    return await user_repository.add_chat(user_chats)
