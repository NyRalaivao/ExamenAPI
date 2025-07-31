from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from datetime import datetime
from typing import List

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"message": "pong"}


@app.get("/home")
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome home!</h1>
    </body>
    </html>
    """


posts: List[dict] = []
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime
@app.post("/posts", status_code=201)
async def create_posts(new_posts: List[Post]):
    posts.extend([post.dict() for post in new_posts])
    return posts

@app.get("/posts")
async def get_posts():
    return posts

@app.put("/posts")
async def update_post(post: Post):
    post_dict = post.dict()
    for i, existing_post in enumerate(posts):
        if existing_post["title"] == post.title:
            posts[i] = post_dict
            return posts

    posts.append(post_dict)
    return posts