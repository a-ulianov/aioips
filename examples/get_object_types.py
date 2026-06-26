"""Пример: получить список типов объектов из метаданных IPS.

Перед запуском задайте подключение и креды через переменные окружения или `.env`
(см. `.env.example`).
"""

import asyncio

from aioips import IPSClient, IPSConfig


async def main() -> None:
    config = IPSConfig()  # читает IPS_* из окружения / .env
    async with IPSClient(config=config) as ips:
        types = await ips.object_types()
        print(f"Всего типов объектов: {len(types)}")
        for object_type in types[:10]:
            print(f"  {object_type.id:>8}  {object_type.object_name}")


if __name__ == "__main__":
    asyncio.run(main())
