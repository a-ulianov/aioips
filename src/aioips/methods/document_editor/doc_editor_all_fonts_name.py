"""Метод получения списка имён всех шрифтов редактора документов."""

from typing import Any

from ...core import APIManager


class DocEditorAllFontsNameMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/getAllFontsName``.

    operationId ``DocumentEditor_GetAllFontsName``.
    """

    async def doc_editor_all_fonts_name(
        self: "DocEditorAllFontsNameMixin",
        *,
        update: bool | None = None,
    ) -> list[str]:
        """Возвращает список имён всех шрифтов, доступных редактору документов.

        Отдаёт перечень наименований шрифтов, известных серверу (из базы данных), для
        использования при оформлении элементов документа. Применяется как справочник
        доступных шрифтов; бинарные данные шрифтов и их метрики этим методом не
        извлекаются.

        Когда применять: чтобы предложить выбор шрифта в интерфейсе редактора или
        проверить наличие нужного шрифта. Метод только читает. Чтобы заставить сервер
        обновить (перечитать) список шрифтов перед выдачей, передайте ``update=True``.

        Args:
            update: Если ``True``, сервер обновит список шрифтов из источника перед
                ответом; если ``False`` — вернёт текущий кэш. Если ``None`` (по
                умолчанию), параметр в запрос не передаётся (поведение сервера по
                умолчанию). Значение сериализуется как ``"true"`` / ``"false"``.

        Returns:
            Список имён шрифтов. Пустой список означает, что доступных шрифтов нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                fonts = await ips.doc_editor_all_fonts_name(update=True)
                print(len(fonts))

        Notes:
            operationId ``DocumentEditor_GetAllFontsName``; путь
            ``GET /core/api/documentEditor/getAllFontsName`` (query ``update``: bool).
        """
        params: dict[str, Any] = {}
        if update is not None:
            params["update"] = str(update).lower()
        data: Any = await self._request(
            "get", "/core/api/documentEditor/getAllFontsName", params=params
        )
        return [str(item) for item in data]
