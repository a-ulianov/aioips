"""Метод чтения настроек типа документа IPS (чтение через POST)."""

from typing import Any

from ...core import APIManager


class DocSettingsMixin(APIManager):
    """Реализует ``POST /core/api/docs/GetSettings``.

    operationId ``Documents_GetSettings``.
    """

    async def doc_settings(
        self: "DocSettingsMixin",
        document_type: int | None = None,
    ) -> dict[str, Any]:
        """Возвращает настройки заданного типа документа (``DocumentTypeSettingsDto``).

        Настройки типа документа описывают правила его обработки: допустимые
        расширения файлов, признаки оформления, выходные типы объектов,
        наследование от конструкторских документов и т. п. Несмотря на
        HTTP-метод POST, это операция ЧТЕНИЯ — сервер ничего не изменяет, тело
        запроса пустое (``{}``), а тип документа передаётся query-параметром
        ``documentType``.

        Когда применять: чтобы прочитать конфигурацию конкретного типа
        документа — в т. ч. перед записью через :meth:`set_doc_settings`
        (обратимая запись по схеме write-same-back). Для нескольких типов сразу
        используйте :meth:`doc_settings_list`. Предусловий нет.

        Args:
            document_type: Идентификатор ТИПА документа (query-параметр
                ``documentType``; это id типа из метаданных, не id
                объекта/версии). ``None`` — параметр не передаётся.

        Returns:
            Словарь ``DocumentTypeSettingsDto`` в исходном виде ответа сервера.
            Пустой словарь ``{}``, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.doc_settings(document_type=1742)

        Notes:
            operationId ``Documents_GetSettings``; путь
            ``POST /core/api/docs/GetSettings``. Ключ query — ``documentType``.
            Тело не передаётся (``{}`` против 415). Возвращается ``dict``, а не
            типизированная модель, чтобы безопасно записать его обратно методом
            :meth:`set_doc_settings`. См. [[ips-object-model]].
        """
        params: dict[str, Any] = {}
        if document_type is not None:
            params["documentType"] = document_type
        data = await self._request("post", "/core/api/docs/GetSettings", params=params, json={})
        return dict(data) if isinstance(data, dict) else {}
