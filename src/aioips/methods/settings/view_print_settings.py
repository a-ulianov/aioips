"""Метод чтения настроек просмотра/печати для типа объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.settings import ViewObjectTypeSettings


class ViewPrintSettingsMixin(APIManager):
    """Реализует ``POST /core/api/settings/view/{objectTypeId}/getSettings``.

    operationId ``Settings_GetViewPrintSettings``.
    """

    async def view_print_settings(
        self: "ViewPrintSettingsMixin", object_type_id: int
    ) -> ViewObjectTypeSettings:
        """Возвращает настройки внедрения данных при просмотре/печати для типа объекта.

        Read-only POST: доменного тела нет, но IPS требует тело, поэтому отправляется
        пустой объект ``{}``; целевой тип задаётся параметром пути ``object_type_id``.
        Метод сообщает, что добавляется в результат просмотра/печати документов данного
        типа: подписи, контрольная сумма файла, набор внедряемых атрибутов.

        Предусловие и id-пространство: ``object_type_id`` — идентификатор ТИПА объекта
        (``objectTypeId``), а не конкретного объекта/версии. Булевы признаки в ответе —
        тристейт: ``None`` означает «наследовать от вышестоящего типа».

        Args:
            object_type_id: Идентификатор типа объекта, для которого читаются настройки
                просмотра/печати. Подставляется в путь URL.

        Returns:
            :class:`~aioips.schemas.settings.ViewObjectTypeSettings` с полями
            ``inject_signs``, ``inject_file_checksum`` (``bool | None``) и
            ``injected_attributes`` (вложенный ``dict | None``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.view_print_settings(1742)
                if settings.inject_signs:
                    ...  # подписи внедряются

        Notes:
            operationId ``Settings_GetViewPrintSettings``; путь
            ``POST /core/api/settings/view/{objectTypeId}/getSettings`` (тело ``{}``).
        """
        payload: dict[str, Any] = {}
        path = f"/core/api/settings/view/{object_type_id}/getSettings"
        data = await self._request("post", path, json=payload)
        return ViewObjectTypeSettings.model_validate(data)
