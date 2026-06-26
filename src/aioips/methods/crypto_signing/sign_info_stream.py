"""Метод получения сведений о подписях объекта."""

from typing import Any

from ...core import APIManager


class SignInfoStreamMixin(APIManager):
    """Реализует ``GET /core/api/cryptoSigning/signInfoStream``.

    operationId ``CryptoSigning_GetSignInfoStream``.
    """

    async def sign_info_stream(
        self: "SignInfoStreamMixin",
        object_id: int,
        graph: str,
    ) -> str:
        """Возвращает поток сведений об электронных подписях объекта.

        Применяют, чтобы получить информацию об уже наложенных на объект ЭЦП (состав
        подписей, сведения о подписантах и сертификатах) в виде сериализованного потока.
        В отличие от :meth:`object_encoded_hash` (данные для НОВОЙ подписи), этот метод
        читает информацию о СУЩЕСТВУЮЩИХ подписях. Глобальные параметры подписания —
        :meth:`signing_settings`.

        Предусловие по id-пространству: ``object_id`` — это идентификатор ОБЪЕКТА
        (``objectID`` / F_OBJECT_ID), а не идентификатор версии. Параметр ``graph``
        обязателен (сервер отвечает 400, если он не передан).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), сведения о
                подписях которого запрашиваются. Не идентификатор версии (``id`` / F_ID).
            graph: Имя графа подписания (набор подписываемых данных/маршрут ЭЦП).
                Обязательный параметр.

        Returns:
            Сведения о подписях объекта в виде строкового потока (сериализованное
            содержимое). Пустая строка означает отсутствие сведений о подписях.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.sign_info_stream(102550, "default")
                # info — сериализованные сведения о подписях объекта

        Notes:
            operationId ``CryptoSigning_GetSignInfoStream``; путь
            ``GET /core/api/cryptoSigning/signInfoStream`` (query ``objectId``,
            ``graph`` — оба обязательны). Ответ в swagger описан как ``string``
            (``format: binary``). См. [[ips-object-model]] (раздел «Идентичность»).
        """
        params: dict[str, Any] = {"objectId": object_id, "graph": graph}
        data = await self._request("get", "/core/api/cryptoSigning/signInfoStream", params=params)
        return "" if data is None else str(data)
