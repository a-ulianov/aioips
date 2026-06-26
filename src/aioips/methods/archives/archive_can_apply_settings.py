"""Метод проверки применимости настроек типов документов к архиву (чтение через POST)."""

from typing import Any

from ...core import APIManager
from ...schemas.archives.permitted_document_types import PermittedDocumentTypes


class ArchiveCanApplySettingsMixin(APIManager):
    """Реализует ``POST /core/api/archives/{archiveId}/canApplySettings``.

    operationId ``Archives_CanApplySettings``.
    """

    async def archive_can_apply_settings(
        self: "ArchiveCanApplySettingsMixin",
        archive_id: int,
        body: PermittedDocumentTypes | dict[str, Any],
    ) -> bool:
        """Проверяет, применимы ли заданные настройки типов документов к архиву (чтение).

        Сообщает, можно ли применить к указанному архиву набор допустимых типов документов
        (с режимом их использования), описанный телом :class:`PermittedDocumentTypes`.
        Несмотря на HTTP-метод POST, это операция ПРОВЕРКИ/ЧТЕНИЯ — сервер ничего не
        изменяет, лишь возвращает признак применимости.

        Когда применять: перед фактическим сохранением настроек архива — чтобы заранее
        убедиться, что выбранный перечень типов документов допустим. Предусловий нет
        (операция чтения/проверки, без побочных эффектов).

        Args:
            archive_id: Идентификатор АРХИВА (``archiveId``, id объекта архива — то, на что
                ссылается атрибут-ссылка «Архив», а не id документа/версии).
            body: Проверяемые настройки (:class:`PermittedDocumentTypes` или эквивалентный
                словарь): перечень типов документов ``documents_types`` и режим их
                применения ``types_using_mode``.

        Returns:
            ``True``, если настройки применимы к архиву, иначе ``False``. При не-булевом
            ответе сервера значение приводится к ``bool``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = PermittedDocumentTypes(
                    documents_types=[1742, 1801], types_using_mode="white"
                )
                ok = await ips.archive_can_apply_settings(1029, settings)
                if ok:
                    ...  # настройки можно сохранять

        Notes:
            operationId ``Archives_CanApplySettings``; путь
            ``POST /core/api/archives/{archiveId}/canApplySettings``; тело —
            ``PermittedDocumentTypesDto``; ответ — ``boolean``. См. объектной модели IPS.
        """
        if isinstance(body, PermittedDocumentTypes):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request(
            "post",
            f"/core/api/archives/{archive_id}/canApplySettings",
            json=payload,
        )
        return bool(data)
