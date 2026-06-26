"""Метод получения сведений о структуре условий выборки по её идентификатору."""

from ...core import APIManager
from ...schemas.search_schemes import ConditionStructureInfo


class ConditionStructureInfoMixin(APIManager):
    """Реализует ``GET /core/api/searchSchemes/{selectionId}/getConditionStructureInfo``.

    operationId ``SearchSchemes_GetConditionStructureInfo``.
    """

    async def condition_structure_info(
        self: "ConditionStructureInfoMixin",
        selection_id: int,
    ) -> list[ConditionStructureInfo]:
        """Возвращает атрибуты, по которым выборка строит условия фильтрации.

        Каждый элемент описывает один атрибут структуры условий выборки
        (``ConditionStructure``): его идентификатор и источник значения. Совокупность
        элементов задаёт набор атрибутов, доступных для условий данной выборки.

        Когда применять: при анализе или построении условий поиска для конкретной
        выборки — чтобы узнать, какие атрибуты в ней участвуют и из каких источников
        (объект, связь, история и т.п.) берутся их значения. Параметры самой выборки
        (типы объектов, колонки, правило версий) даёт :meth:`search_scheme`.

        Args:
            selection_id: Идентификатор выборки (selection), для которой
                запрашивается структура условий.

        Returns:
            Список элементов :class:`ConditionStructureInfo`. Пустой список означает,
            что у выборки нет атрибутов в структуре условий. Значимые поля каждого
            элемента: ``attribute_id`` — идентификатор атрибута,
            ``attribute_source_types`` — источник его значения.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если выборка не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                infos = await ips.condition_structure_info(1024)
                attr_ids = [info.attribute_id for info in infos]

        Notes:
            operationId ``SearchSchemes_GetConditionStructureInfo``; путь
            ``GET /core/api/searchSchemes/{selectionId}/getConditionStructureInfo``
            (тело — массив ``ConditionStructureInfoDto``).
        """
        path = f"/core/api/searchSchemes/{selection_id}/getConditionStructureInfo"
        data = await self._request("get", path)
        return [ConditionStructureInfo.model_validate(item) for item in data]
