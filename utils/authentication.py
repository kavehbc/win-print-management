from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
import json
import os
from pathlib import Path

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))


def read_users_db():
    users_db_file = dir_path.parent / "users.json"
    with open(users_db_file, 'r', encoding="utf-8") as outfile:
        users_db = json.loads(outfile.read())
    return users_db


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")


def authenticate(form_data: OAuth2PasswordRequestForm):
    users_db = read_users_db()
    user = users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password = form_data.password
    if not password == user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user["username"], "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    users_db = read_users_db()
    token = users_db.get(token)
    if token:
        user = User(**token)
    else:
        user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
