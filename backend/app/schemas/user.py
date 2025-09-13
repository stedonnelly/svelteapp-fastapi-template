from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    email: EmailStr | None = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None

    model_config = {"from_attributes": True}

class LoginIn(BaseModel):
    username: str
    password: str

