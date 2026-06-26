"""Метод включения объектов в состав версии-проекта."""

from typing import Any

from ...core import APIManager
from ...schemas.relations import Relation


class ObjectIncludeInCompositionMixin(APIManager):
    """Реализует ``.../includeInComposition`` (``Objects_IncludeInComposition``)."""

    async def object_include_in_composition(
        self: "ObjectIncludeInCompositionMixin",
        project_version_id: int,
        part_ids: list[int],
        *,
        log_history: bool = True,
    ) -> list[Relation]:
        """Включает версии-потомки в состав версии-проекта (МУТИРУЮЩАЯ операция).

        Создаёт связи «родитель → потомок» в составе изделия: добавляет указанные версии
        потомков в состав версии-проекта (родителя). Возвращает созданные связи. Учтите
        двухуровневую идентичность IPS: родитель здесь задаётся идентификатором ВЕРСИИ-проекта,
        а потомки — идентификаторами ВЕРСИЙ объектов (а не их ``ObjectID``).

        Предусловие: версия-проект обычно должна быть в режиме редактирования (см.
        :meth:`object_check_out` / :meth:`object_edit`), иначе сервер отклонит изменение
        состава.

        Args:
            project_version_id: Идентификатор ВЕРСИИ объекта-проекта (родителя), в состав
                которого включаются потомки (``ID`` версии, не ``ObjectID``).
            part_ids: Идентификаторы ВЕРСИЙ объектов-потомков, добавляемых в состав
                (передаются телом запроса как ``list[int]``).
            log_history: Журналировать ли операцию в истории модификаций
                (query ``isNeedToLogModificationHistory``).

        Returns:
            Список созданных связей :class:`~aioips.schemas.relations.Relation` (родитель →
            потомок); пустой список, если сервер ничего не вернул.

        Raises:
            IPSConflictError: Если версия-проект не в режиме редактирования либо нарушены
                правила применяемости/состава.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                relations = await ips.object_include_in_composition(102551, [33001, 33002])

        References:
            ``Objects_IncludeInComposition``. Связанные: :meth:`object_composition_with_params`,
            :meth:`object_check_out`, :meth:`object_edit`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/{project_version_id}/includeInComposition",
            json=part_ids,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return [Relation.model_validate(x) for x in (result or [])]
