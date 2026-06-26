"""Метод назначения базовыми сразу нескольких версий объектов."""

from typing import Any

from ...core import APIManager


class ObjectMakeBaseVersionsMixin(APIManager):
    """Реализует ``POST /core/api/objects/makeBaseVersion`` (``Objects_MakeBaseVersions``)."""

    async def object_make_base_versions(
        self: "ObjectMakeBaseVersionsMixin",
        object_ids: list[int],
        *,
        log_history: bool = True,
        ignore_exceptions: bool | None = None,
    ) -> list[int]:
        """Делает указанные версии объектов базовыми (МУТИРУЮЩАЯ, пакетная операция).

        Назначает базовой (актуальной) ту версию объекта, что передана в списке: после этого
        именно она используется по умолчанию при разрешении версий. Пакетный вариант
        :meth:`object_make_base_version` — обрабатывает сразу несколько объектов за один вызов.

        Args:
            object_ids: Идентификаторы ВЕРСИЙ объектов, назначаемых базовыми (передаются
                телом запроса как ``list[int]``).
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).
            ignore_exceptions: Игнорировать ошибки по отдельным объектам и продолжать
                (query ``isNeedToIgnoreExceptions``); ``None`` — параметр не передаётся.

        Returns:
            Список идентификаторов объектов, для которых операция выполнена; пустой список,
            если сервер ничего не вернул.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                done = await ips.object_make_base_versions([33001, 33002])

        References:
            ``Objects_MakeBaseVersions``. Связанные: :meth:`object_make_base_version`,
            :meth:`object_base_version`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        if ignore_exceptions is not None:
            params["isNeedToIgnoreExceptions"] = str(ignore_exceptions).lower()
        data = await self._request(
            "post", "/core/api/objects/makeBaseVersion", json=object_ids, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return [int(x) for x in result] if result else []
