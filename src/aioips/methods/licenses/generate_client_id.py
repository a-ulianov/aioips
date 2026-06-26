"""Метод генерации идентификатора клиента для лицензирования IPS."""

from ...core import APIManager


class GenerateClientIdMixin(APIManager):
    """Реализует метод ``GET /core/api/licenses/generateClientId``.

    operationId ``Licenses_GenerateClientId``.
    """

    async def generate_client_id(self: "GenerateClientIdMixin") -> str:
        """Генерирует на сервере новый идентификатор клиента для лицензирования IPS.

        Сервер формирует и возвращает уникальный идентификатор клиента (client id),
        используемый в процедурах активации/привязки лицензии IPS. Значение
        вырабатывается сервером при каждом вызове; метод не принимает параметров.

        Когда применять: на шаге получения/привязки лицензии, когда требуется
        предъявить серверу идентификатор клиента (например, при формировании запроса
        активации). Вызов читающий и идемпотентный по побочным эффектам, но возвращаемое
        значение может различаться между вызовами.

        Returns:
            Идентификатор клиента в виде строки. Если сервер вернул пустой ответ
            (``null``), метод отдаёт пустую строку ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                client_id = await ips.generate_client_id()
                print(client_id)

        Notes:
            operationId ``Licenses_GenerateClientId``; путь
            ``GET /core/api/licenses/generateClientId`` (скалярная строка).
        """
        data = await self._request("get", "/core/api/licenses/generateClientId")
        return "" if data is None else str(data)
