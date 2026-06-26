"""Метод получения системной палитры цветов виджетов форм."""

from ...core import APIManager
from ...schemas.forms import WidgetColor


class SystemColorsMixin(APIManager):
    """Реализует ``GET /core/api/forms/getSystemColors`` (``Forms_GetSystemColors``)."""

    async def system_colors(self: "SystemColorsMixin") -> list[WidgetColor]:
        """Возвращает системную палитру цветов для оформления виджетов форм.

        Системная палитра — предопределённый набор именованных цветов платформы IPS
        (в отличие от настраиваемой пользовательской палитры из :meth:`widget_colors`).
        Каждый элемент содержит имя, строковое RGBA-представление и компоненты
        ``r``/``g``/``b``/``a``. Предусловий нет.

        Когда применять: чтобы показать системные цвета в редакторе формы или
        интерпретировать ссылку на системный цвет по его имени.

        Returns:
            Список цветов по схеме :class:`WidgetColor`. Пустой список означает, что
            системная палитра не определена.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                colors = await ips.system_colors()
                print([c.color_name for c in colors])

        Notes:
            operationId ``Forms_GetSystemColors``; путь
            ``GET /core/api/forms/getSystemColors``; ответ — массив ``WidgetColor``.
        """
        data = await self._request("get", "/core/api/forms/getSystemColors")
        return [WidgetColor.model_validate(item) for item in data]
