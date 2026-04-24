from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import mysql.connector # pyright: ignore[reportMissingImports]
import os

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password123@db_mongo:27017")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db_mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "app_db")

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client.blog_db

@app.get("/posts")
async def get_posts():
    cursor = mongo_db.posts.find({}, {"_id": 0})
    posts = await cursor.to_list(length=100)
    return posts

@app.get("/users")
def get_users():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateurs")
    users = cursor.fetchall()
    conn.close()
    return users