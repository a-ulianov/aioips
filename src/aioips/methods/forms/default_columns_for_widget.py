"""Метод получения колонок по умолчанию для табличного виджета."""

from ...core import APIManager
from ...schemas.forms import WidgetGridColumn


class DefaultColumnsForWidgetMixin(APIManager):
    """Реализует ``GET /core/api/forms/getDefaultColumns4Widget``.

    operationId ``Forms_GetDefaultColumns4Widget``.
    """

    async def default_columns_for_widget(
        self: "DefaultColumnsForWidgetMixin",
    ) -> list[WidgetGridColumn]:
        """Возвращает набор колонок по умолчанию для табличного виджета.

        Колонки по умолчанию — стандартная раскладка таблицы (grid-виджета): какие
        колонки показывать, к каким атрибутам они привязаны и в каком порядке. Это
        шаблон, применяемый при создании нового табличного виджета.

        Когда применять: при настройке/инициализации табличного виджета на форме —
        чтобы получить базовый состав колонок. Параметры не требуются. Результат
        интерпретируется схемой :class:`WidgetGridColumn`.

        Returns:
            Список колонок по схеме :class:`WidgetGridColumn`. Пустой список означает,
            что колонки по умолчанию не заданы.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                columns = await ips.default_columns_for_widget()
                for c in columns:
                    print(c.scheme, c.attr_type, c.is_virtual)

        Notes:
            operationId ``Forms_GetDefaultColumns4Widget``; путь
            ``GET /core/api/forms/getDefaultColumns4Widget``; ответ — массив
            ``WidgetGridColumn``.
        """
        data = await self._request("get", "/core/api/forms/getDefaultColumns4Widget")
        return [WidgetGridColumn.model_validate(item) for item in data]
