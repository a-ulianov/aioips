"""Метод записи настроек документов типа объекта (config-мутация, confirm-гейт)."""

from typing import Any

from ...core import APIManager
from ...schemas.documents import DocumentSettings


class SaveDocumentSettingsMixin(APIManager):
    """Реализует ``POST /api/documents/{objectTypeId}/settings``.

    operationId ``DocumentSettings_SaveDocumentSettings``.
    """

    async def save_document_settings(
        self: "SaveDocumentSettingsMixin",
        object_type_id: int,
        settings: DocumentSettings | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки документов для ТИПА объекта (МУТИРУЮЩАЯ, ``confirm``).

        Парная запись к чтению :meth:`document_settings`: сохраняет, как формируются и
        ведут себя документы данного ТИПА объекта (прототипы, правила генерации). Настройка
        уровня ТИПА — влияет на все объекты типа, поэтому защищена ``confirm``: без
        ``confirm=True`` поднимается :class:`ValueError` ещё до обращения к серверу.

        Обратимость: прочитайте текущие настройки через :meth:`document_settings`,
        сохраните снимок, измените нужное и запишите; для отката запишите снимок обратно
        (write-same-back при тех же значениях не меняет состояние).

        Args:
            object_type_id: Идентификатор ТИПА объекта (``objectTypeId``), а не
                конкретного объекта/версии. Подставляется в путь URL.
            settings: Настройки (:class:`DocumentSettings`) или эквивалентный словарь
                (``DocumentSettingsContract``). Для точного round-trip передавайте снимок,
                прочитанный :meth:`document_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cur = await ips.document_settings(1742)          # бэкап
                await ips.save_document_settings(1742, cur, confirm=True)

        Notes:
            operationId ``DocumentSettings_SaveDocumentSettings``; путь
            ``POST /api/documents/{objectTypeId}/settings`` (НЕ ``/core/api``); тело —
            ``DocumentSettingsContract``. Парный read — :meth:`document_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "save_document_settings мутирует настройки документов типа; передайте confirm=True"
            )
        if isinstance(settings, DocumentSettings):
            payload: Any = settings.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = settings
        await self._request("post", f"/api/documents/{object_type_id}/settings", json=payload)
        return None
