from fastapi import FastAPI
from routers import new
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(new.router)


# 允许的来源（可以是域名列表）
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-frontend-domain.com"  # 你的服务器IP/域名
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[origins],      # 生成环境
    allow_origins=["*"],      # 允许访问的源
    allow_credentials=True,   # 允许携带 Cookie
    allow_methods=["*"],      # 允许所有请求方法
    allow_headers=["*"],      # 允许所有请求头
)