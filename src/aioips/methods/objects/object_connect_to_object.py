"""Метод присоединения объекта к другому объекту."""

from typing import Any

from ...core import APIManager


class ObjectConnectToObjectMixin(APIManager):
    """Реализует ``.../objects/{objectId}/connectToObject`` (``Objects_ConnectToObject``)."""

    async def object_connect_to_object(
        self: "ObjectConnectToObjectMixin",
        object_id: int,
        *,
        to_object_id: int | None = None,
        log_history: bool = True,
    ) -> int:
        """Присоединяет один объект к другому (МУТИРУЮЩАЯ операция).

        Связывает объект ``object_id`` с объектом ``to_object_id`` на стороне сервера
        (доменная привязка одного объекта к другому). Возвращает целочисленный код/идентификатор
        результата операции.

        Args:
            object_id: Идентификатор присоединяемого ОБЪЕКТА (``F_OBJECT_ID``).
            to_object_id: Идентификатор ОБЪЕКТА-приёмника (``F_OBJECT_ID``), к которому идёт
                присоединение (query ``toObjectId``); ``None`` — параметр не передаётся
                (серверный дефолт).
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).

        Returns:
            Целочисленный код/идентификатор результата операции (``0``, если сервер вернул
            пустой результат).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                code = await ips.object_connect_to_object(102550, to_object_id=102560)

        References:
            ``Objects_ConnectToObject``.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        if to_object_id is not None:
            params["toObjectId"] = str(to_object_id)
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/connectToObject", json={}, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return int(result) if result is not None else 0
