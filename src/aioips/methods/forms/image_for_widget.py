"""Метод получения изображения виджета по версии."""

from typing import Any

from ...core import APIManager


class ImageForWidgetMixin(APIManager):
    """Реализует ``GET /core/api/forms/getImage4Widget`` (``Forms_GetImage4Widget``)."""

    async def image_for_widget(
        self: "ImageForWidgetMixin",
        version_id: int,
    ) -> str:
        """Возвращает изображение виджета по идентификатору версии (строкой).

        Изображение виджета — графика, привязанная к виджету формы (как правило,
        строка с данными изображения, например base64). Сервер отдаёт скалярную
        строку; обёртка нормализует ``None`` в пустую строку.

        Предусловие по id-пространству: аргумент — идентификатор ВЕРСИИ
        (``versionId`` / F_ID) соответствующего объекта, а НЕ идентификатор объекта.

        Когда применять: чтобы получить графическое представление виджета по его версии
        (например, для предпросмотра в редакторе формы).

        Args:
            version_id: Идентификатор ВЕРСИИ (``versionId`` / F_ID), для которой
                запрашивается изображение виджета. Не идентификатор объекта.

        Returns:
            Строка с изображением виджета. Пустая строка (``""``), если изображение
            отсутствует (сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                image = await ips.image_for_widget(102551)
                if image:
                    ...  # декодировать/использовать изображение

        Notes:
            operationId ``Forms_GetImage4Widget``; путь
            ``GET /core/api/forms/getImage4Widget`` (query ``versionId``);
            ответ — строка (``string``).
        """
        params: dict[str, Any] = {"versionId": version_id}
        data = await self._request("get", "/core/api/forms/getImage4Widget", params=params)
        return "" if data is None else str(data)
