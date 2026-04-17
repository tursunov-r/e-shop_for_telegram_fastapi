import re
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    model_validator,
)


class UserCreateSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)
    balance: float = Field(default=0, ge=0, le=1_000_000)

    @field_validator("password")
    @classmethod
    def validate_password(cls, pwd: str):
        pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]).{8,}$'
        )
        if not pattern.match(pwd):
            raise ValueError(
                "Password must contain lowercase and uppercase letters, numbers and special characters."
            )
        return pwd

    @model_validator(mode="after")
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match.")
        return self


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserCreateResponseSchema(BaseModel):
    message: str
