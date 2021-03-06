import typing

from fastapi import HTTPException
from pydantic import BaseModel, validator


class User(BaseModel):
    MAX_USERNAME_SIZE: typing.ClassVar = 20

    username: str

    @validator("username")
    def validate_username_length(cls, username):
        if len(username) > User.MAX_USERNAME_SIZE:
            raise HTTPException(status_code=400,
                                detail="Username length must not exceed {}.".format(User.MAX_USERNAME_SIZE))
        return username

    @validator("username")
    def validate_username_emptiness(cls, username):
        if len(username) == 0:
            raise HTTPException(status_code=400, detail="Username cannot be empty.")
        return username

    class Config:
        orm_mode = True


class Message(BaseModel):
    MAX_TEXT_SIZE: typing.ClassVar = 100

    text: str
    sender: str
    recipient: str

    @validator("text")
    def validate_text_length(cls, text):
        if len(text) > Message.MAX_TEXT_SIZE:
            raise HTTPException(status_code=400,
                                detail="Message length must not exceed {}.".format(Message.MAX_TEXT_SIZE))
        return text

    @validator("text")
    def validate_text_emptiness(cls, text):
        if len(text) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")
        return text

    @validator("sender")
    def validate_sender(cls, sender):
        User(username=sender)
        return sender

    @validator("recipient")
    def validate_recipient(cls, recipient):
        User(username=recipient)
        return recipient

    class Config:
        orm_mode = True
