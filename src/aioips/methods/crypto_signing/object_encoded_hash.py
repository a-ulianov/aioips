"""Метод получения кодированного хэша объекта для ЭЦП."""

from typing import Any

from ...core import APIManager
from ...schemas.crypto_signing import CryptoProviderInfo


class ObjectEncodedHashMixin(APIManager):
    """Реализует ``GET /core/api/cryptoSigning/objectEncodedHash``.

    operationId ``CryptoSigning_GetObjectEncodedHash``.
    """

    async def object_encoded_hash(
        self: "ObjectEncodedHashMixin",
        object_id: int,
        graph: str,
        alg_id: int,
        crypto_provider: CryptoProviderInfo,
    ) -> str:
        """Возвращает кодированный хэш объекта — исходные данные для формирования ЭЦП.

        Первый шаг подписания объекта электронной цифровой подписью: сервер вычисляет
        хэш подписываемого содержимого объекта и возвращает его в кодированном виде.
        Этот хэш передаётся криптопровайдеру/токену клиента, который формирует по нему
        подпись; готовую подпись затем отправляют методом создания ЭЦП. Связанные
        сведения об уже существующих подписях объекта — :meth:`sign_info_stream`,
        глобальные параметры подписания — :meth:`signing_settings`.

        Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
        (``objectID`` / F_OBJECT_ID), а не идентификатор версии. Параметры ``graph`` и
        ``alg_id`` обязательны (сервер отвечает 400 при их отсутствии); сведения о
        криптопровайдере передаются телом запроса.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), хэш которого
                вычисляется. Не идентификатор версии (``id`` / F_ID).
            graph: Имя графа подписания (набор подписываемых данных/маршрут ЭЦП).
                Обязательный параметр.
            alg_id: Числовой идентификатор алгоритма хэширования. Обязательный параметр.
            crypto_provider: Сведения о криптопровайдере и ключевом контейнере
                (:class:`CryptoProviderInfo`), которыми будет вычисляться подпись.

        Returns:
            Кодированный хэш объекта строкой — данные для последующего вычисления ЭЦП на
            стороне клиента. Пустая строка означает отсутствие данных для подписи.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                provider = CryptoProviderInfo(provider_type=75, key_number=1)
                encoded = await ips.object_encoded_hash(102550, "default", 1, provider)
                # encoded — кодированный хэш, передаётся криптопровайдеру для подписи

        Notes:
            operationId ``CryptoSigning_GetObjectEncodedHash``; путь
            ``GET /core/api/cryptoSigning/objectEncodedHash`` (query ``objectId``,
            ``graph``, ``algId`` — обязательны; тело — ``CryptoProviderInfoDTO``). См.
            [[ips-object-model]] (раздел «Идентичность»).
        """
        params: dict[str, Any] = {"objectId": object_id, "graph": graph, "algId": alg_id}
        body = crypto_provider.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "get", "/core/api/cryptoSigning/objectEncodedHash", json=body, params=params
        )
        return "" if data is None else str(data)
