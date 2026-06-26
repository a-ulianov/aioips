"""Метод чтения настроек нескольких типов документов IPS (чтение через POST)."""

from typing import Any

from ...core import APIManager


class DocSettingsListMixin(APIManager):
    """Реализует ``POST /core/api/docs/GetSettingsList``.

    operationId ``Documents_GetSettingsList``.
    """

    async def doc_settings_list(
        self: "DocSettingsListMixin",
        document_type_ids: list[int],
    ) -> list[dict[str, Any]]:
        """Возвращает настройки для перечня типов документов одним запросом (чтение).

        Пакетный аналог :meth:`doc_settings`: по списку идентификаторов типов
        документов отдаёт их настройки (``DocumentTypeSettingsDto`` на каждый
        тип). Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ — сервер ничего
        не изменяет; перечень типов передаётся телом-списком.

        Когда применять: чтобы прочитать настройки сразу нескольких типов
        документов, избегая множества вызовов :meth:`doc_settings`. Предусловий
        нет.

        Args:
            document_type_ids: Список идентификаторов ТИПОВ документов (id типов
                из метаданных, не id объектов/версий). Передаётся телом запроса
                (``json``-массив целых).

        Returns:
            Список словарей ``DocumentTypeSettingsDto`` в исходном виде ответа
            сервера. Каждый элемент приводится к ``dict``. Пустой список ``[]``,
            если настроек нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.doc_settings_list([1742, 1801])

        Notes:
            operationId ``Documents_GetSettingsList``; путь
            ``POST /core/api/docs/GetSettingsList``. Тело — массив int
            (``json=document_type_ids``). Элементы возвращаются как ``dict``
            (не типизированная модель) для единообразия с :meth:`doc_settings`.
            См. объектной модели IPS.
        """
        data = await self._request("post", "/core/api/docs/GetSettingsList", json=document_type_ids)
        items = data if isinstance(data, list) else []
        return [dict(item) for item in items]
