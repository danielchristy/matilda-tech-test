# test_db.py
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

async def test_conn():
    url = os.getenv("DATABASE_URL")
    print("Trying to connect to:", url)
    try:
        conn = await asyncpg.connect(url)
        print("✅ Connected successfully!")
        await conn.close()
    except Exception as e:
        print("❌ Failed to connect:", e)

asyncio.run(test_conn())
