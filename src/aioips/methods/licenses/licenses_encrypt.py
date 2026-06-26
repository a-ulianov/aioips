"""Метод шифрования лицензионных данных IPS (POST, чтение/преобразование)."""

from ...core import APIManager
from ...schemas.licenses.encrypt import EncryptLicense


class LicensesEncryptMixin(APIManager):
    """Реализует метод ``POST /core/api/licenses/encrypt`` (``Licenses_Encrypt``)."""

    async def licenses_encrypt(
        self: "LicensesEncryptMixin",
        data: EncryptLicense,
    ) -> str:
        """Шифрует лицензионные данные на сервере и возвращает зашифрованную строку.

        Выполняет серверное шифрование переданной полезной нагрузки лицензии для
        конкретного приложения (``app_id``) и клиента (``client_id``). Несмотря на
        POST-глагол, это операция ЧТЕНИЯ/преобразования: чистая функция без состояния —
        сервер ничего не сохраняет и не меняет, лишь возвращает результат шифрования.
        Поэтому вызов идемпотентен по побочным эффектам.

        Когда применять: на этапе клиентской подготовки лицензионных данных, когда нужно
        зашифровать полезную нагрузку перед её предъявлением (например, в связке с
        идентификатором клиента из :meth:`generate_client_id`).

        Args:
            data: Тело запроса :class:`EncryptLicense` с полями ``app_id`` (идентификатор
                приложения), ``client_id`` (идентификатор клиента) и
                ``data_as_base64_string`` (полезная нагрузка в Base64). Сериализуется как
                JSON c camelCase-алиасами; ``None``-поля исключаются.

        Returns:
            Зашифрованную строку. Сервер отдаёт скалярный JSON-результат; если пришло
            не строковое значение, оно приводится к строке (``str``).

        Raises:
            IPSError: При ошибочном ответе сервера (например, 400 при некорректных данных).

        Example:
            async with IPSClient(config=config) as ips:
                payload = EncryptLicense(
                    app_id=42,
                    client_id=await ips.generate_client_id(),
                    data_as_base64_string="QkFTRTY0",
                )
                encrypted = await ips.licenses_encrypt(payload)

        Notes:
            ``operationId``: ``Licenses_Encrypt``; путь ``POST /core/api/licenses/encrypt``.
            Связанные методы: :meth:`generate_client_id`.
        """
        body = data.model_dump(mode="json", by_alias=True, exclude_none=True)
        result = await self._request("post", "/core/api/licenses/encrypt", json=body)
        return result if isinstance(result, str) else str(result)
