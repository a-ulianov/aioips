"""Метод получения колонок грида проекта (Improject)."""

from ...core import APIManager
from ...schemas.improjects import DisplayedColumns


class GridColumnsMixin(APIManager):
    """Реализует ``GET /core/api/improjects/grid-columns``.

    ``operationId`` ``ImProject_GetGridColumns``.
    """

    async def grid_columns(self: "GridColumnsMixin") -> DisplayedColumns:
        """Возвращает набор колонок табличного представления (грида) проектов Improject.

        Назначение: получить, какие колонки и в каком порядке показывать в гриде
        проекта управления проектами. Применяйте для построения шапки таблицы
        задач на клиенте/в MCP-инструменте перед загрузкой самого проекта через
        :meth:`project`. Метод не привязан к конкретному проекту и не требует
        идентификатора — отдаёт общие настройки колонок.

        Предусловие: модуль Improject (управление проектами) должен быть
        лицензирован.

        Returns:
            :class:`DisplayedColumns`. Поле ``columns`` — список колонок
            (``ColumnDto``) в виде «сырых» словарей; значимые ключи: ``id`` —
            строковый идентификатор колонки, ``width`` — ширина в пикселях
            (может отсутствовать). Пустой список означает отсутствие настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cols = await ips.grid_columns()
                print([c["id"] for c in cols.columns])

        Notes:
            ``operationId``: ``ImProject_GetGridColumns``; путь
            ``GET /core/api/improjects/grid-columns`` (ответ ``DisplayedColumnsDto``).
            Связанные методы: :meth:`project` (сам проект с задачами).
        """
        data = await self._request("get", "/core/api/improjects/grid-columns")
        return DisplayedColumns.model_validate(data)
