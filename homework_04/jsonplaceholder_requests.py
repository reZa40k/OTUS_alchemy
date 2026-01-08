from logger import log
import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users/"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts/"


async def fetch_api(url: str) -> list[dict]:
    """Возвращает результат запроса к API"""
    log.info(f"Запрос к {url}")
    async with (
        aiohttp.ClientSession() as session,
        session.get(url) as response,
    ):
        res = await response.json()
    log.info(f"Получен результат запроса к {url}")
    return res


async def fetch_user() -> list[dict]:
    """Асинхронный запрос пользователей"""
    return await fetch_api(USERS_DATA_URL)


async def fetch_post() -> list[dict]:
    """Асинхронный запрос постов"""
    return await fetch_api(POSTS_DATA_URL)
