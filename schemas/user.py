from pydantic import BaseModel

class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: str

class UserDetails(BaseModel):
    user_id: str
    full_name: str
    email: str
    phone: str
    profile_picture: str