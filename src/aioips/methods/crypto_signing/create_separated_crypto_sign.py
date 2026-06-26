"""Метод создания отделённой (separated) криптографической подписи объекта."""

from typing import Any

from ...core import APIManager


class CreateSeparatedCryptoSignMixin(APIManager):
    """Реализует ``POST /core/api/cryptoSigning/createSeparatedCryptoSign``.

    operationId ``CryptoSigning_CreateSeparatedCryptoSign``.
    """

    async def create_separated_crypto_sign(
        self: "CreateSeparatedCryptoSignMixin",
        object_id: int,
        request: dict[str, Any],
        eds_as_string: str,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Создаёт отделённую (separated) ЭЦП объекта (МУТИРУЮЩАЯ, ``confirm``).

        Формирует на сервере ОТДЕЛЁННУЮ криптографическую подпись для объекта,
        заданного параметром ``object_id``, и сохраняет результат как артефакт IPS.
        В отличие от :meth:`create_crypto_sign` (встроенная подпись), здесь подпись
        хранится отдельно от подписываемых данных. Это создающая, изменяющая состояние
        операция: по умолчанию НЕ выполняется — требуется явный ``confirm=True``, иначе
        поднимается :class:`ValueError` ещё ДО обращения к серверу. Доступные провайдеры
        и настройки подписания читают :meth:`signing_settings`.

        Предусловие: на сервере должны быть настроены сертификаты и криптопровайдер
        (CSP); без рабочей конфигурации подписания вызов завершится ошибкой. Тело
        ``request`` (``CryptoSignInfoDTO``) описывает параметры подписи (см.
        :meth:`create_crypto_sign`).

        Args:
            object_id: Идентификатор объекта для подписи (обязательный query-параметр
                ``objectId``, ``int64``). Указывает версию объекта, для которой
                создаётся отделённая подпись.
            request: Тело запроса ``CryptoSignInfoDTO`` в виде словаря; отправляется
                как JSON-тело.
            eds_as_string: Строковое представление ЭЦП/сертификата (обязательный
                query-параметр ``edsAsString``), идентифицирующее ключ подписи.
            confirm: Подтверждение операции создания артефакта. Без ``True`` метод не
                делает запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``dict[str, Any]`` по схеме ``CryptoSigningResultDTO``: ключевые поля
            ``signedObjectId``, ``signObjectId`` и ``errorMessage``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибке сервера (нет сертификатов/CSP, неверный объект и т. п.).

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.create_separated_crypto_sign(
                    102550,
                    {"signedObject": 102550, "userID": 7, "rankID": 1},
                    eds_as_string="<сертификат-как-строка>",
                    confirm=True,
                )
                print(result["signObjectId"], result.get("errorMessage"))

        Notes:
            operationId ``CryptoSigning_CreateSeparatedCryptoSign``; путь
            ``POST /core/api/cryptoSigning/createSeparatedCryptoSign`` (query
            ``objectId``, ``edsAsString``; тело ``CryptoSignInfoDTO``; ответ
            ``CryptoSigningResultDTO``). Связанные: :meth:`create_crypto_sign`,
            :meth:`signing_settings`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Создание отделённой ЭЦП изменяет данные на сервере: передайте confirm=True"
            )
        params: dict[str, Any] = {
            "objectId": str(object_id),
            "edsAsString": eds_as_string,
        }
        data = await self._request(
            "post",
            "/core/api/cryptoSigning/createSeparatedCryptoSign",
            json=request,
            params=params,
        )
        return data if isinstance(data, dict) else {}
