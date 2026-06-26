"""Метод проверки потомка типа: id потомка + GUID родителя."""

from urllib.parse import quote

from ...core import APIManager


class IsObjectTypeChildByChildIdParentGuidMixin(APIManager):
    """Реализует ``GET .../isChild/byChildId/{childTypeId}/byParentGuid/{parentTypeGuid}``."""

    async def is_object_type_child_by_child_id_parent_guid(
        self: "IsObjectTypeChildByChildIdParentGuidMixin",
        child_type_id: int,
        parent_type_guid: str,
    ) -> bool:
        """Проверяет, является ли тип потомком другого: id потомка + GUID родителя.

        Смешанная адресация варианта :meth:`is_object_type_child`: потомок задаётся
        локальным ``id``, а родитель — переносимым GUID. Проверяет, входит ли
        ``child_type_id`` в поддерево типа с GUID ``parent_type_guid`` (на любой глубине).
        GUID родителя кодируется в URL. Ответ сервера — голое булево значение.

        Когда применять: когда родительский тип известен по стабильному GUID (из
        конфигурации между средами), а потомок — по локальному ``id``. Оба по id —
        :meth:`is_object_type_child`; оба по GUID — :meth:`is_object_type_child_by_guids`.

        Args:
            child_type_id: Идентификатор предполагаемого ДОЧЕРНЕГО типа (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).
            parent_type_guid: GUID предполагаемого РОДИТЕЛЬСКОГО типа (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            ``True`` — ``child_type_id`` входит в поддерево родителя с заданным GUID;
            ``False`` — не входит (в т.ч. при отсутствии одного из типов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_child = await ips.is_object_type_child_by_child_id_parent_guid(
                    1742, "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(is_child)

        Notes:
            operationId ``Metadata_IsObjectTypeChildOfByChildIdParentGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/isChild/byChildId/{childTypeId}/``
            ``byParentGuid/{parentTypeGuid}`` (ответ — ``boolean``). См.
            объектной модели IPS. Связанные методы: :meth:`is_object_type_child`,
            :meth:`is_object_type_child_by_guids`.
        """
        encoded_guid = quote(parent_type_guid, safe="")
        path = (
            f"/core/api/metadata/objectTypeTree/isChild/byChildId/{child_type_id}/"
            f"byParentGuid/{encoded_guid}"
        )
        data = await self._request("get", path)
        return bool(data) if data is not None else False
