from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import null
from sqlalchemy.ext.asyncio.session import AsyncSession

from config.db_config import get_db
from crud import users
from schemas.users import UserRequest

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    db_user = await users.get_user_by_username(db, user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # 新增用户
    user = await users.create_user(db, user_data)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": None,
            "userInfo": {
                "id": user.id,
                "username": user_data.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }
