from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Request
from libs.schemas.chat import (
    Chat,
    ChatCreate,
    ChatAddUsers,
)
from libs.schemas.message import (
    Message,
)
from app.services.chat_repository import ChatRepository
from app.services.message_repository import MessageRepository

router = APIRouter()
chat_repository = ChatRepository()
message_repository = MessageRepository()


@router.get('/{chat_id}', responses={
    200: {"model": Chat},
})
async def get_chat_info(request: Request,
                        chat_id: UUID) -> Chat:
    return await chat_repository.get_chat(request, chat_id)


@router.post('', responses={
    201: {"model": Chat},
})
async def create_chat(request: Request,
                      chat: ChatCreate) -> Chat:
    return await chat_repository.create_chat(request, chat)


@router.post('/add-users', responses={
    201: {"model": Chat},
})
async def add_users_to_chat(request: Request,
                            chat_users: ChatAddUsers) -> Chat:
    return await chat_repository.add_users_to_chat(request, chat_users)


@router.get('/{chat_id}/messages', responses={
    200: {"model": list[Message]},
})
async def get_chat_messages(request: Request,
                            chat_id: UUID,
                            message_timestamp: datetime = None,
                            start_timestamp: datetime = None,
                            end_timestamp: datetime = None,
                            ) -> list[Message]:
    if message_timestamp:
        return await message_repository.get_message(request,
                                                    chat_id,
                                                    message_timestamp)

    return await message_repository.get_messages(request,
                                                 chat_id,
                                                 start_timestamp,
                                                 end_timestamp)


@router.post('/{chat_id}/messages', responses={
    201: {"model": Message},
})
async def create_message(request: Request,
                         message: Message) -> Message:
    return await message_repository.create_message(request, message)
