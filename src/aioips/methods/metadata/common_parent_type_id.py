"""Метод получения id ближайшего общего предка для пары типов объектов."""

from ...core import APIManager


class CommonParentTypeIdMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/commonParent/{childType1Id}/{childType2Id}/id``."""

    async def common_parent_type_id(
        self: "CommonParentTypeIdMixin",
        child_type1_id: int,
        child_type2_id: int,
    ) -> int:
        """Возвращает id ближайшего ОБЩЕГО предка для пары типов объектов.

        Находит в дереве ТИПОВ наименьший общий предок (lowest common ancestor) двух
        заданных типов — ближайший тип, в поддерево которого входят оба. Полезно для
        определения общего супертипа, к которому можно привести оба типа. Ответ сервера —
        целое число.

        Когда применять: для поиска общего базового типа пары (например, чтобы выбрать
        обобщённую обработку для двух подтипов), проверки их совместимости по иерархии.
        Цепочки предков по отдельности — :meth:`parent_type_ids`; корень ветви одного
        типа — :meth:`top_parent_type_id`.

        Args:
            child_type1_id: Идентификатор ПЕРВОГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).
            child_type2_id: Идентификатор ВТОРОГО типа объекта (``ObjectTypeID``,
                то же id-пространство ТИПОВ объектов).

        Returns:
            Идентификатор ближайшего общего предка (``ObjectTypeID``). ``0`` — общего
            предка нет (типы из разных корневых ветвей) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                common_id = await ips.common_parent_type_id(1742, 1801)
                print(common_id)

        Notes:
            operationId ``Metadata_GetCommonParentObjectTypeIdByIdPair``; путь
            ``GET /core/api/metadata/objectTypeTree/commonParent/{childType1Id}/``
            ``{childType2Id}/id`` (ответ — ``int``). См. [[ips-object-model]].
            Связанные методы: :meth:`parent_type_ids`, :meth:`top_parent_type_id`.
        """
        path = (
            f"/core/api/metadata/objectTypeTree/commonParent/{child_type1_id}/{child_type2_id}/id"
        )
        data = await self._request("get", path)
        return int(data) if data is not None else 0
