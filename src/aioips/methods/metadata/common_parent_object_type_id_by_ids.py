"""Метод поиска общего родительского типа для набора типов по их id."""

from ...core import APIManager


class CommonParentObjectTypeIdByIdsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/commonParent/byIds/id``."""

    async def common_parent_object_type_id_by_ids(
        self: "CommonParentObjectTypeIdByIdsMixin",
        object_type_ids: list[int],
    ) -> int:
        """Возвращает id ближайшего общего родительского типа для НАБОРА типов по их id.

        Пакетный аналог :meth:`common_parent_type_id` (пара типов): находит ближайший общий
        тип-предок в дереве типов сразу для произвольного набора типов. Полезно для
        обобщения разнородной выборки до единого надтипа. Операция ЧТЕНИЯ метамодели: POST
        используется лишь для передачи списка id телом, дерево не изменяется.

        Когда применять: когда нужно вычислить минимальный общий тип для группы объектов
        разных типов (например, чтобы подобрать общий набор атрибутов или общий фильтр).
        Аналог по id ВЕРСИЙ объектов — :meth:`common_parent_object_type_id_by_version_ids`.

        Args:
            object_type_ids: Список id ТИПОВ объектов (``ObjectTypeID``; локальные).
                Передаётся телом запроса (JSON-массив).

        Returns:
            id ближайшего общего родительского ТИПА (``ObjectTypeID``). ``0`` — общего
            предка нет (``null`` от сервера) либо входной список пуст/некорректен.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                common_id = await ips.common_parent_object_type_id_by_ids([1742, 1801, 1850])
                print(common_id)

        Notes:
            operationId ``Metadata_GetCommonParentObjectTypeIdByIds``; путь
            ``POST /core/api/metadata/objectTypeTree/commonParent/byIds/id`` (тело —
            ``list[int]`` id ТИПОВ; ответ — ``int``). См. [[ips-object-model]]. Связанные
            методы: :meth:`common_parent_object_type_id_by_version_ids`,
            :meth:`common_parent_type_id`.
        """
        path = "/core/api/metadata/objectTypeTree/commonParent/byIds/id"
        data = await self._request("post", path, json=object_type_ids)
        return int(data) if data is not None else 0
