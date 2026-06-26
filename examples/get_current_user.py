"""Пример: получить информацию о текущем пользователе сессии.

Перед запуском задайте подключение и креды через переменные окружения или `.env`
(см. `.env.example`): IPS_BASE_URL, IPS_LOGIN_NAME, IPS_PASSWORD, IPS_ROLE_NAME.
"""

import asyncio

from aioips import IPSClient, IPSConfig


async def main() -> None:
    config = IPSConfig()  # читает IPS_* из окружения / .env
    async with IPSClient(config=config) as ips:
        me = await ips.user_info()
        print(f"Логин: {me.login_name}")
        print(f"Имя:   {me.user_name}")
        print(f"Админ: {me.is_admin}")


if __name__ == "__main__":
    asyncio.run(main())
