"""Метод создания криптографической подписи объекта (ЭЦП)."""

from typing import Any

from ...core import APIManager


class CreateCryptoSignMixin(APIManager):
    """Реализует ``POST /core/api/cryptoSigning/createCryptoSign``.

    operationId ``CryptoSigning_CreateCryptoSign``.
    """

    async def create_crypto_sign(
        self: "CreateCryptoSignMixin",
        request: dict[str, Any],
        eds_as_string: str,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Создаёт криптографическую подпись (ЭЦП) объекта (МУТИРУЮЩАЯ, ``confirm``).

        Формирует на сервере встроенную (прикреплённую) криптографическую подпись для
        указанного объекта и сохраняет результат как артефакт в IPS. Это создающая,
        изменяющая состояние операция: по умолчанию НЕ выполняется — требуется явный
        ``confirm=True``, иначе поднимается :class:`ValueError` ещё ДО обращения к
        серверу. Применяйте, когда нужно подписать объект целиком; для отделённой
        (separated) подписи используйте :meth:`create_separated_crypto_sign`. Доступные
        криптопровайдеры и текущие настройки подписания читают
        :meth:`signing_settings` (см. также :meth:`object_encoded_hash`).

        Предусловие: на сервере должны быть настроены сертификаты и криптопровайдер
        (CSP); без рабочей конфигурации подписания вызов завершится ошибкой. Тело
        ``request`` (``CryptoSignInfoDTO``) описывает параметры подписи: подписываемый
        объект (``signedObject`` — id ВЕРСИИ объекта), пользователя (``userID``), ранг
        подписи (``rankID``), графику/разрешение штампа (``graph``/``resolution``).

        Args:
            request: Тело запроса ``CryptoSignInfoDTO`` (см. поля выше) в виде
                словаря; отправляется как JSON-тело.
            eds_as_string: Строковое представление ЭЦП/сертификата (обязательный
                query-параметр ``edsAsString``), идентифицирующее ключ подписи.
            confirm: Подтверждение операции создания артефакта. Без ``True`` метод не
                делает запрос и поднимает :class:`ValueError` (защитный гейт).

        Returns:
            ``dict[str, Any]`` по схеме ``CryptoSigningResultDTO``: ключевые поля
            ``signedObjectId`` (id подписанного объекта), ``signObjectId`` (id объекта
            подписи) и ``errorMessage`` (текст ошибки подписания, если есть).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибке сервера (нет сертификатов/CSP, неверный объект и т. п.).

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.create_crypto_sign(
                    {"signedObject": 102550, "userID": 7, "rankID": 1},
                    eds_as_string="<сертификат-как-строка>",
                    confirm=True,
                )
                print(result["signObjectId"], result.get("errorMessage"))

        Notes:
            operationId ``CryptoSigning_CreateCryptoSign``; путь
            ``POST /core/api/cryptoSigning/createCryptoSign`` (query ``edsAsString``;
            тело ``CryptoSignInfoDTO``; ответ ``CryptoSigningResultDTO``). Связанные:
            :meth:`create_separated_crypto_sign`, :meth:`signing_settings`,
            :meth:`object_encoded_hash`. См. [[ips-object-model]].
        """
        if confirm is not True:
            raise ValueError("Создание ЭЦП изменяет данные на сервере: передайте confirm=True")
        params: dict[str, Any] = {"edsAsString": eds_as_string}
        data = await self._request(
            "post",
            "/core/api/cryptoSigning/createCryptoSign",
            json=request,
            params=params,
        )
        return data if isinstance(data, dict) else {}
