"""Метод получения всех версий объекта по идентификатору."""

from ...core import APIManager
from ...schemas.objects import AllObjectVersionsParameters, ObjectSelectResult


class ObjectsAllVersionsMixin(APIManager):
    """Реализует ``POST /core/api/objects/allObjectVersions``.

    Соответствует операции ``Objects_GetAllObjectVersions``.
    """

    async def objects_all_versions(
        self: "ObjectsAllVersionsMixin",
        params: AllObjectVersionsParameters,
    ) -> list[ObjectSelectResult]:
        """Возвращает все версии объекта (история) по его идентификатору.

        Применяйте, когда нужна полная линейка версий одного объекта: рабочая,
        предыдущие, при необходимости — заготовки и удалённые. В отличие от
        :meth:`object_get` (отдаёт одну базовую версию по ``objectID``), этот метод
        перечисляет все версии и возвращает их в том же компактном формате, что и
        :meth:`objects_select` (id + значения запрошенных атрибутов). Только чтение —
        это POST, но БЕЗ мутаций (тело несёт параметры выборки).

        Предусловие по id-пространству (важно): объект (или одну из его версий)
        задаёт ``params.id``, а трактовка ``id`` управляется флагом
        ``params.is_object_id`` (см. :class:`AllObjectVersionsParameters`). Формулировки
        в swagger противоречивы — проверяйте поведение на проде.

        Args:
            params: Параметры выборки версий (см. :class:`AllObjectVersionsParameters`):
                ``id`` (объект/версия), ``is_object_id`` (трактовка ``id``),
                ``show_blanks`` / ``show_deleted`` (включать заготовки/удалённые),
                ``attribute_ids`` (какие атрибуты вернуть). Сериализуется в тело запроса.

        Returns:
            Список версий по схеме :class:`ObjectSelectResult` (пустой список, если
            версий не найдено). У каждого элемента — ``object_id`` версии и
            ``attributes`` (значения запрошенных в ``attribute_ids`` атрибутов).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import AllObjectVersionsParameters

            async with IPSClient(config=config) as ips:
                versions = await ips.objects_all_versions(
                    AllObjectVersionsParameters(id=102550, attribute_ids=[9, 10]),
                )
                for v in versions:
                    print(v.object_id, v.values)

        Notes:
            ``operationId``: ``Objects_GetAllObjectVersions``. Ответ — «голый» массив
            ``ObjectsSelectResultDto`` (как у :meth:`objects_select`), разворачивается
            напрямую. См. объектной модели IPS (раздел «Идентичность») и
            :meth:`object_get`.
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/objects/allObjectVersions", json=payload)
        items = data if isinstance(data, list) else []
        return [ObjectSelectResult.model_validate(item) for item in items]
