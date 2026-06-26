"""Метод получения имени типа связи по идентификатору."""

from ...core import APIManager


class RelationTypeMetaNameMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/relationTypes/{id}/name``."""

    async def relation_type_meta_name(
        self: "RelationTypeMetaNameMixin",
        relation_type_id: int,
    ) -> str:
        """Возвращает прямое имя типа связи по его идентификатору.

        Лёгкая выборка одного поля: прямое имя связи (``type_name``, например
        «Входит в») без загрузки полного описания. Обратное имя той же связи в этот
        результат не входит — за ним обращайтесь к :meth:`relation_type_meta`
        (поле ``reverse_name``). Ответ сервера — голая строка.

        Когда применять: для отображения имени типа связи в UI/логах, когда известен
        только ``id``. За полным метаописанием — :meth:`relation_type_meta`.

        Args:
            relation_type_id: Идентификатор типа связи (``RelationType`` —
                id-пространство ТИПОВ связей, не ``RelationID`` конкретной связи).

        Returns:
            Прямое имя типа связи. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.relation_type_meta_name(501)
                print(name)

        Notes:
            operationId ``Metadata_GetRelationTypeNameById``; путь
            ``GET /core/api/metadata/relationTypes/{id}/name`` (ответ — ``string``).
            Аналог по GUID — :meth:`relation_type_meta_name_by_guid`.
        """
        path = f"/core/api/metadata/relationTypes/{relation_type_id}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
