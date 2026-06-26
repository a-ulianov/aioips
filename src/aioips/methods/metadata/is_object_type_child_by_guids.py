"""Метод проверки потомка типа по GUID потомка и GUID родителя."""

from urllib.parse import quote

from ...core import APIManager


class IsObjectTypeChildByGuidsMixin(APIManager):
    """Реализует ``GET .../isChild/byChildGuid/{childTypeGuid}/byParentGuid/{parentTypeGuid}``."""

    async def is_object_type_child_by_guids(
        self: "IsObjectTypeChildByGuidsMixin",
        child_type_guid: str,
        parent_type_guid: str,
    ) -> bool:
        """Проверяет, является ли тип потомком другого (оба адресуются по GUID).

        Полностью GUID-ориентированный вариант :meth:`is_object_type_child`: и потомок,
        и родитель задаются переносимыми GUID. Проверяет, входит ли тип
        ``child_type_guid`` в поддерево типа ``parent_type_guid`` (на любой глубине).
        Оба GUID кодируются в URL. Ответ сервера — голое булево значение.

        Когда применять: для проверки отношения предок–потомок между типами по стабильным
        GUID, без привязки к локальным ``id`` инсталляции (сверка конфигурации между
        средами). Оба по id — :meth:`is_object_type_child`; смешанно (id потомка + GUID
        родителя) — :meth:`is_object_type_child_by_child_id_parent_guid`.

        Args:
            child_type_guid: GUID предполагаемого ДОЧЕРНЕГО типа (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.
            parent_type_guid: GUID предполагаемого РОДИТЕЛЬСКОГО типа (строка того же
                формата); кодируется в URL.

        Returns:
            ``True`` — тип ``child_type_guid`` входит в поддерево ``parent_type_guid``;
            ``False`` — не входит (в т.ч. при отсутствии одного из типов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_child = await ips.is_object_type_child_by_guids(
                    "cad001c5-306c-11d8-b4e9-00304f19f545",
                    "b1f2e3d4-0000-11d8-b4e9-00304f19f545",
                )
                print(is_child)

        Notes:
            operationId ``Metadata_IsObjectTypeChildOfByChildGuidParentGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/isChild/byChildGuid/{childTypeGuid}/``
            ``byParentGuid/{parentTypeGuid}`` (ответ — ``boolean``). См.
            [[ips-object-model]]. Связанные методы: :meth:`is_object_type_child`,
            :meth:`is_object_type_child_by_child_id_parent_guid`.
        """
        encoded_child = quote(child_type_guid, safe="")
        encoded_parent = quote(parent_type_guid, safe="")
        path = (
            f"/core/api/metadata/objectTypeTree/isChild/byChildGuid/{encoded_child}/"
            f"byParentGuid/{encoded_parent}"
        )
        data = await self._request("get", path)
        return bool(data) if data is not None else False
