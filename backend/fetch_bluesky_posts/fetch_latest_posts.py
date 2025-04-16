# まずは atproto ライブラリをインストールします
# pip install atproto

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from atproto import Client
from dotenv import load_dotenv
import os

# 環境変数を読み込む
load_dotenv()

my_handle = os.environ.get('BLUE_SKY_HANDLE')
my_app_password = os.environ.get('BLUE_SKY_APP_PASSWORD')

app = FastAPI()

class PostRequest(BaseModel):
    target_userid: str
    limit: Optional[int] = 100

@app.post("/get_posts")
def get_latest_posts(req: PostRequest):
    client = Client()
    client.login(my_handle, my_app_password)

    response = client.app.bsky.feed.get_author_feed(
        actor=req.target_userid,
        limit=req.limit
    )

    return {"posts": response.data["feed"]}
