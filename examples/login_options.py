"""Пример: узнать доступные роли и уровни доступа для логина (без пароля).

Полезно, чтобы заранее определить идентификатор роли перед аутентификацией.
Требуется только IPS_BASE_URL; пароль не нужен.
"""

import asyncio

from aioips import IPSClient, IPSConfig


async def main() -> None:
    # Для этого вызова достаточно базового URL; авторизация не требуется,
    # поэтому передаём фиктивный токен, чтобы пройти валидацию конфигурации.
    config = IPSConfig(access_token="not-used")  # base_url берётся из окружения
    async with IPSClient(config=config) as ips:
        options = await ips.login_options("your-login")
        print("Доступные роли:")
        for role in options.roles:
            print(f"  {role.id:>8}  {role.name}")
        print("Уровни доступа:")
        for level in options.access_levels:
            print(f"  {level.id:>8}  {level.name}")


if __name__ == "__main__":
    asyncio.run(main())
