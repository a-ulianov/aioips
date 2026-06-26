"""Метод получения GUID непосредственного родительского типа по GUID потомка."""

from urllib.parse import quote

from ...core import APIManager


class ParentTypeGuidByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parent/byGuid/{childTypeGuid}/guid``."""

    async def parent_type_guid_by_guid(
        self: "ParentTypeGuidByGuidMixin",
        child_type_guid: str,
    ) -> str:
        """Возвращает GUID НЕПОСРЕДСТВЕННОГО родительского типа по GUID потомка.

        Полностью GUID-ориентированный вариант :meth:`parent_type_id`: один шаг вверх по
        дереву ТИПОВ, где и потомок (вход), и родитель (выход) адресуются переносимыми
        GUID. Возвращает GUID прямого родителя (тип на один уровень выше). GUID
        кодируется в URL. Ответ сервера — строка.

        Когда применять: для навигации вверх по иерархии типов на один уровень по
        стабильным GUID, без привязки к локальным ``id`` инсталляции. Родитель в виде
        id — :meth:`parent_type_id`; вся цепочка предков в GUID —
        :meth:`parent_type_guids_by_guid`.

        Args:
            child_type_guid: GUID ДОЧЕРНЕГО типа объекта (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``); кодируется в URL.

        Returns:
            GUID непосредственного родительского типа (строка в id-пространстве ТИПОВ
            объектов). Пустая строка — у типа нет родителя (корневой) либо не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent_guid = await ips.parent_type_guid_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(parent_guid)

        Notes:
            operationId ``Metadata_GetObjectTypeParentGuidByGuid``; путь
            ``GET /core/api/metadata/objectTypeTree/parent/byGuid/{childTypeGuid}/guid``
            (ответ — строка). См. объектной модели IPS (иерархия типов).
            Связанные методы: :meth:`parent_type_id`,
            :meth:`parent_type_guids_by_guid`.
        """
        encoded_guid = quote(child_type_guid, safe="")
        path = f"/core/api/metadata/objectTypeTree/parent/byGuid/{encoded_guid}/guid"
        data = await self._request("get", path)
        return str(data) if data is not None else ""
