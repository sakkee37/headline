from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


# 检查收藏状态
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")


# 添加收藏
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")
