from pydantic import BaseModel

# Schema for login request
class UserLogin(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_id: int

    class Config:
        orm_mode = True