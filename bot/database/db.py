import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    await create_tables()


async def create_tables():
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            BIGSERIAL PRIMARY KEY,
                tg_id         BIGINT UNIQUE NOT NULL,
                username      TEXT,
                full_name     TEXT NOT NULL,
                phone         TEXT,
                age           INTEGER,
                course        TEXT,
                registered_at TIMESTAMP DEFAULT NOW()
            );
        """)


async def get_user(tg_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE tg_id=$1", tg_id)


async def get_user_by_phone(phone: str):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE phone=$1", phone)


async def delete_user(tg_id: int):
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM users WHERE tg_id=$1", tg_id)
        return result  # "DELETE 1" yoki "DELETE 0"


async def register_user(tg_id, username, full_name, phone, age, course):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (tg_id, username, full_name, phone, age, course)
            VALUES ($1,$2,$3,$4,$5,$6)
            ON CONFLICT (tg_id) DO UPDATE
            SET full_name=$3, phone=$4, age=$5, course=$6
        """, tg_id, username, full_name, phone, age, course)


async def get_all_users():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM users ORDER BY registered_at DESC")
