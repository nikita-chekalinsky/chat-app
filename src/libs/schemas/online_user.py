from pydantic import BaseModel


class UserDevice(BaseModel):
    notification_sender_id: str
    device_name: str = None


class OnlineUser(BaseModel):
    user_id: str
    is_online: bool
    user_devices: list[UserDevice] = []
