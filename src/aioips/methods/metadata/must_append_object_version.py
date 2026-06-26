"""Метод проверки необходимости добавлять версию объекта в контекст редактирования."""

from ...core import APIManager


class MustAppendObjectVersionMixin(APIManager):
    """Реализует ``GET .../editingContext/mustAppendObjectVersion/{id}``."""

    async def must_append_object_version(
        self: "MustAppendObjectVersionMixin",
        id: int,
    ) -> bool:
        """Проверяет, нужно ли добавлять версию объекта в контекст редактирования (по id).

        Контекст редактирования — набор типов объектов, правящихся совместно. Для некоторых
        типов правка требует включения в контекст не объекта целиком, а конкретной ВЕРСИИ
        объекта (F_ID, а не F_OBJECT_ID). Метод отвечает, должен ли тип объекта с данным
        ``id`` добавлять версию объекта в контекст редактирования. Ответ сервера — голое
        булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: при сборке контекста для checkout — чтобы решить, передавать id
        версии или id объекта (см. двухуровневую идентичность IPS: версия vs объект).
        Признак простоты контекста — :meth:`is_simple_editing_context`.

        Args:
            id: Идентификатор типа объекта (id-пространство ТИПОВ объектов метаданных,
                не id объекта и не id версии конкретного экземпляра).

        Returns:
            ``True`` — в контекст редактирования нужно добавлять версию объекта; ``False`` —
            не нужно (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.must_append_object_version(42):
                    print("в контекст передаём id версии, а не id объекта")

        Notes:
            operationId ``Metadata_MustAppendVersionToEditingContext``; путь
            ``GET /core/api/metadata/editingContext/mustAppendObjectVersion/{id}`` (ответ —
            ``boolean``). Связанный метод: :meth:`is_simple_editing_context`.
        """
        path = f"/core/api/metadata/editingContext/mustAppendObjectVersion/{id}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
