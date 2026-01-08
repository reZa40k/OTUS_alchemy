import asyncio
from jsonplaceholder_requests import fetch_post, fetch_user
from models import async_engine, Base
from logger import log
from models import Session, User, Post
from sqlalchemy.ext.asyncio import AsyncSession


async def create_clear_tables():
    """Создаём пустые таблицы в базе данных"""
    async with async_engine.connect() as conn:
        async with conn.begin():
            log.info("Дропаем все таблицы")
            await conn.run_sync(Base.metadata.drop_all)
            log.info("Создаём все таблицы")
            await conn.run_sync(Base.metadata.create_all)


async def get_users_and_posts() -> tuple[list[dict], list[dict]]:
    """Получаем пользователей и посты через gather"""
    users, posts = await asyncio.gather(
        fetch_user(),
        fetch_post(),
    )
    log.info(f"Получены пользователи и посты через gather")
    return users, posts


async def add_users_and_posts(
    users: list[dict],
    posts: list[dict],
    session: AsyncSession,
):
    """Добавляем пользователей и посты в базу данных"""
    users_obj = [
        User(
            username=user["username"],
            email=user["email"],
            name=user["name"],
        )
        for user in users
    ]

    posts_obj = [
        Post(
            title=post["title"],
            body=post["body"],
            user_id=post["userId"],
        )
        for post in posts
    ]
    log.info("Добавляем пользователей и посты в базу данных")
    session.add_all(users_obj)
    session.add_all(posts_obj)
    await session.commit()
    log.info("Пользователи и посты добавлены в базу данных")


async def async_main():
    await create_clear_tables()
    users, posts = await get_users_and_posts()
    async with Session() as session:
        await add_users_and_posts(users, posts, session)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
