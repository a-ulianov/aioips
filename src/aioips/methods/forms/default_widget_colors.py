"""Метод получения палитры цветов виджетов по умолчанию."""

from ...core import APIManager
from ...schemas.forms import WidgetColor


class DefaultWidgetColorsMixin(APIManager):
    """Реализует ``GET /core/api/forms/getDefaultWidgetColors``.

    operationId ``Forms_GetDefaultWidgetColors``.
    """

    async def default_widget_colors(
        self: "DefaultWidgetColorsMixin",
    ) -> list[WidgetColor]:
        """Возвращает палитру цветов виджетов по умолчанию.

        Палитра по умолчанию — рекомендуемый стандартный набор именованных цветов для
        оформления виджетов на формах. Отличается от пользовательской палитры
        (:meth:`widget_colors`) и системной (:meth:`system_colors`) источником: это
        предустановленные значения по умолчанию.

        Когда применять: чтобы предложить базовый выбор цвета при оформлении виджета,
        либо сопоставить сохранённое имя цвета с RGBA-значением из набора по умолчанию.
        Параметры не требуются.

        Returns:
            Список цветов по схеме :class:`WidgetColor`. Пустой список означает, что
            палитра по умолчанию не настроена.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                colors = await ips.default_widget_colors()
                palette = {c.color_name: c.color_rgba for c in colors}

        Notes:
            operationId ``Forms_GetDefaultWidgetColors``; путь
            ``GET /core/api/forms/getDefaultWidgetColors``; ответ — массив ``WidgetColor``.
        """
        data = await self._request("get", "/core/api/forms/getDefaultWidgetColors")
        return [WidgetColor.model_validate(item) for item in data]
