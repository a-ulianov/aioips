"""Метод проверки, является ли контекст редактирования простым по id."""

from ...core import APIManager


class IsSimpleEditingContextMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/editingContext/isSimple/{id}``."""

    async def is_simple_editing_context(
        self: "IsSimpleEditingContextMixin",
        id: int,
    ) -> bool:
        """Проверяет, является ли контекст редактирования типа объекта простым (по id).

        Контекст редактирования — набор типов объектов, правящихся совместно. «Простой»
        контекст — это вырожденный случай: правка затрагивает только сам объект, без
        подтягивания подчинённых типов в общую транзакцию (упрощённый сценарий checkout).
        Метод отвечает, является ли контекст типа объекта с данным ``id`` простым. Ответ
        сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы отличить лёгкую правку (только сам объект) от сложной
        (совместная правка нескольких типов) и выбрать соответствующий сценарий checkout.
        Сам факт наличия контекста — :meth:`is_editing_context`; нужно ли добавлять версию —
        :meth:`must_append_object_version`.

        Args:
            id: Идентификатор типа объекта (id-пространство ТИПОВ объектов метаданных,
                не id объекта и не id версии).

        Returns:
            ``True`` — контекст редактирования простой (правится только сам объект);
            ``False`` — нет (в том числе если сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.is_simple_editing_context(42):
                    print("checkout затронет только сам объект")

        Notes:
            operationId ``Metadata_IsSimpleEditingContext``; путь
            ``GET /core/api/metadata/editingContext/isSimple/{id}`` (ответ — ``boolean``).
            Связанные методы: :meth:`is_editing_context`,
            :meth:`must_append_object_version`.
        """
        path = f"/core/api/metadata/editingContext/isSimple/{id}"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
