from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
app = FastAPI(
    title="TrenDp"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'Alice'},
    {'id': 3, 'role': 'trader', 'name': 'Matt', 'degree': [
        {'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}
    ]},
]

class TypeDegree(Enum):
    newbie = 'newbie'
    expert = 'expert'

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: TypeDegree
class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = None

@app.get('/users/{user_id}', response_model=List[User])
def get_users(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]

@app.post('/users')
def reaname_user(user_id: int, name: str):
    renamed_user = next(filter(lambda user: user.get('id') == user_id, fake_users))
    renamed_user['name'] = name
    return renamed_user