from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from models.news import Category, News
from sqlalchemy import func, update

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # # 先尝试从缓存中获取数据
    # cached_categories = await get_cached_categories()
    # if cached_categories:
    #     return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # ORM

    # # 写入缓存
    # if categories:
    #     categories = jsonable_encoder(categories)
    #     await set_cache_categories(categories)

    # 返回数据
    return categories


async def get_news_list(
        db: AsyncSession,
        category_id: int,
        skip: int = 0,
        limit: int = 10
):
    # # 先尝试从缓存获取新闻列表
    # # 跳过的数量skip = (页码 - 1) * 每页数量 -> 页码 = 跳过的数量 // 每页数量 + 1
    # # await get_cache_news_list(分类id, 页码, 每页数量)
    #
    # page = skip // limit + 1
    # cached_list = await get_cache_news_list(category_id, page, limit)  # 缓存数据 json
    # if cached_list:
    #     # return cached_list  # 要的是 ORM
    #     return [News(**item) for item in cached_list]

    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # # 写入缓存
    # if news_list:
    #     # 先把 ORM 数据 转换 字典才能写入缓存
    #     # ORM 转成 Pydantic，再转为 字典
    #     # by_alias=False 不适用别名，保存 Python 风格，因为 Redis 数据是给后端用的
    #     news_data = [
    #         NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False)
    #         for item in news_list
    #     ]
    #     await set_cache_news_list(category_id, page, limit, news_data)
    #
    return news_list

# 获取新闻总数
async def get_news_count(
        db:AsyncSession,
        category_id : int
):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错



# 获取新闻详情
async def get_news_detail(
        db: AsyncSession,
        new_id : int
):
    # # 先尝试从缓存获取新闻详情
    # cached_detail = await get_cached_news_detail(new_id)
    # if cached_detail:
    #     return News(**cached_detail)

    # 查询数据库
    stmt = select(News).where(News.id == new_id)
    result = await db.execute(stmt)
    news = result.scalar_one_or_none()
    #
    # # 写入缓存
    # if news:
    #     news_data = jsonable_encoder(news)
    #     await cache_news_detail(new_id, news_data)

    return news

# 新闻浏览量 +1
async def increase_new_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 → 检查数据库是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0
