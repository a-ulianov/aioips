"""Метод поиска общего родительского типа для набора объектов по id их версий."""

from ...core import APIManager


class CommonParentObjectTypeIdByVersionIdsMixin(APIManager):
    """Реализует ``POST .../objectTypeTree/commonParent/byVersionIds/id``."""

    async def common_parent_object_type_id_by_version_ids(
        self: "CommonParentObjectTypeIdByVersionIdsMixin",
        version_ids: list[int],
    ) -> int:
        """Возвращает id ближайшего общего родительского типа для объектов по id их версий.

        Как :meth:`common_parent_object_type_id_by_ids`, но на входе — не id ТИПОВ, а id
        ВЕРСИЙ объектов: сервер сам определяет тип каждого объекта и находит ближайший общий
        тип-предок в дереве типов. Удобно, когда на руках есть конкретные объекты (их
        версии), а их типы заранее неизвестны. Операция ЧТЕНИЯ метамодели: POST используется
        лишь для передачи списка id телом, дерево не изменяется.

        Предусловие по id-пространству (важно): передаются id ВЕРСИЙ (``id`` / F_ID,
        ``int64``), а НЕ id объектов (``objectID``) и НЕ id типов. Типичный источник — поля
        ``id`` из DTO объектов или результатов поиска.

        Когда применять: чтобы обобщить выбранные пользователем объекты до единого надтипа,
        не вычисляя их типы вручную. Аналог по id ТИПОВ —
        :meth:`common_parent_object_type_id_by_ids`.

        Args:
            version_ids: Список id ВЕРСИЙ объектов (``id`` / F_ID; ``int64``). Передаётся
                телом запроса (JSON-массив).

        Returns:
            id ближайшего общего родительского ТИПА (``ObjectTypeID``). ``0`` — общего
            предка нет (``null`` от сервера) либо входной список пуст/некорректен.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                common_id = await ips.common_parent_object_type_id_by_version_ids(
                    [102550, 102551]
                )
                print(common_id)

        Notes:
            operationId ``Metadata_GetCommonParentObjectTypeIdByVersionIds``; путь
            ``POST /core/api/metadata/objectTypeTree/commonParent/byVersionIds/id`` (тело —
            ``list[int]`` id ВЕРСИЙ; ответ — ``int``). См. [[ips-object-model]] (раздел
            «Идентичность»). Связанные методы:
            :meth:`common_parent_object_type_id_by_ids`.
        """
        path = "/core/api/metadata/objectTypeTree/commonParent/byVersionIds/id"
        data = await self._request("post", path, json=version_ids)
        return int(data) if data is not None else 0
