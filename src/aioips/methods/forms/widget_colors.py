"""Метод получения пользовательской палитры цветов виджетов форм."""

from ...core import APIManager
from ...schemas.forms import WidgetColor


class WidgetColorsMixin(APIManager):
    """Реализует ``GET /core/api/forms/getColors`` (``Forms_GetColors``)."""

    async def widget_colors(self: "WidgetColorsMixin") -> list[WidgetColor]:
        """Возвращает пользовательскую палитру цветов для оформления виджетов форм.

        Палитра — набор именованных цветов, доступных при оформлении виджетов на формах.
        Каждый элемент содержит имя, строковое RGBA-представление и компоненты
        ``r``/``g``/``b``/``a``. Это пользовательская (настраиваемая) палитра; системную
        неизменяемую палитру отдаёт :meth:`system_colors`. Предусловий нет.

        Когда применять: чтобы предложить выбор цвета в редакторе формы или сопоставить
        сохранённое имя цвета с его RGBA-значением.

        Returns:
            Список цветов по схеме :class:`WidgetColor`. Пустой список означает, что
            пользовательская палитра не настроена.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                colors = await ips.widget_colors()
                palette = {c.color_name: c.color_rgba for c in colors}

        Notes:
            operationId ``Forms_GetColors``; путь ``GET /core/api/forms/getColors``;
            ответ — массив ``WidgetColor``.
        """
        data = await self._request("get", "/core/api/forms/getColors")
        return [WidgetColor.model_validate(item) for item in data]
