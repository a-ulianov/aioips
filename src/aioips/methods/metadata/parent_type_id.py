"""Метод получения id непосредственного родительского типа объекта."""

from ...core import APIManager


class ParentTypeIdMixin(APIManager):
    """Реализует ``GET .../objectTypeTree/parent/{childTypeId}/id``."""

    async def parent_type_id(
        self: "ParentTypeIdMixin",
        child_type_id: int,
    ) -> int:
        """Возвращает id НЕПОСРЕДСТВЕННОГО родительского типа в иерархии типов.

        Один шаг вверх по дереву ТИПОВ: для заданного типа возвращает идентификатор его
        прямого родителя (тип на один уровень выше). В отличие от :meth:`parent_type_ids`
        (вся цепочка предков) — только ближайший родитель. Ответ сервера — целое число.

        Когда применять: для навигации вверх по иерархии на один уровень, определения
        непосредственного супертипа. Вся цепочка предков — :meth:`parent_type_ids`;
        корневой предок ветви — :meth:`top_parent_type_id`; адресация по GUID потомка —
        :meth:`parent_type_guid_by_guid`.

        Args:
            child_type_id: Идентификатор ДОЧЕРНЕГО типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID`` экземпляра).

        Returns:
            Идентификатор непосредственного родительского типа (``ObjectTypeID``).
            ``0`` — у типа нет родителя (корневой тип) либо тип не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parent_id = await ips.parent_type_id(1742)
                print(parent_id)

        Notes:
            operationId ``Metadata_GetObjectTypeParentIdById``; путь
            ``GET /core/api/metadata/objectTypeTree/parent/{childTypeId}/id``
            (ответ — ``int``). См. [[ips-object-model]] (иерархия типов).
            Связанные методы: :meth:`parent_type_ids`, :meth:`top_parent_type_id`,
            :meth:`parent_type_guid_by_guid`.
        """
        path = f"/core/api/metadata/objectTypeTree/parent/{child_type_id}/id"
        data = await self._request("get", path)
        return int(data) if data is not None else 0
