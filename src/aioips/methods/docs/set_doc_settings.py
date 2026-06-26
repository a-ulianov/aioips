"""Метод записи настроек типа документа IPS (мутация)."""

from typing import Any

from ...core import APIManager


class SetDocSettingsMixin(APIManager):
    """Реализует ``POST /core/api/docs/SetSettings``.

    operationId ``Documents_SetSettings``.
    """

    async def set_doc_settings(
        self: "SetDocSettingsMixin",
        settings: dict[str, Any],
        *,
        document_type: int | None = None,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки заданного типа документа (МУТАЦИЯ).

        Перезаписывает конфигурацию типа документа (``DocumentTypeSettingsDto``):
        допустимые расширения файлов, признаки оформления, выходные типы
        объектов, наследование и т. п. Это операция ЗАПИСИ, изменяющая
        серверное состояние.

        Обратимость: операция ОБРАТИМА по схеме write-same-back — прочитайте
        текущие настройки методом :meth:`doc_settings` и для отката запишите их
        обратно тем же методом :meth:`set_doc_settings`. Перед изменением
        рекомендуется сохранить исходный ``DocumentTypeSettingsDto``.

        Защита: меняет настройки на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            settings: Новые настройки типа документа — словарь
                ``DocumentTypeSettingsDto`` (как его отдаёт :meth:`doc_settings`).
                Передаётся телом запроса (``json=settings``) без преобразований.
            document_type: Идентификатор ТИПА документа (query-параметр
                ``documentType``; id типа из метаданных, не id объекта/версии).
                ``None`` — параметр не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.doc_settings(document_type=1742)
                # ... изменить нужные поля current ...
                await ips.set_doc_settings(
                    current, document_type=1742, confirm=True
                )

        Notes:
            operationId ``Documents_SetSettings``; путь
            ``POST /core/api/docs/SetSettings``. Ключ query — ``documentType``;
            тело — ``DocumentTypeSettingsDto`` (``json=settings``). Ответ — void
            (None). См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "set_doc_settings меняет настройки типа документа; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if document_type is not None:
            params["documentType"] = document_type
        await self._request("post", "/core/api/docs/SetSettings", params=params, json=settings)
        return None
