"""Метод записи настроек видимости объекта (мутирующий, обратимый)."""

from ...core import APIManager
from ...schemas.visibilities import VisibilitySettings


class ObjectUpdateVisibilitySettingsMixin(APIManager):
    """Реализует ``Visibility_UpdateVisibilitySettings`` (запись настроек видимости)."""

    async def object_update_visibility_settings(
        self: "ObjectUpdateVisibilitySettingsMixin",
        object_id: int,
        settings: list[VisibilitySettings],
    ) -> None:
        """Сохраняет настройки видимости объекта (что показано/скрыто в дереве/UI).

        МУТИРУЮЩАЯ операция: перезаписывает, какие связанные узлы объекта видимы или
        скрыты и какие значки им сопоставлены. Парная запись к чтению
        :meth:`object_visibilities`: прочитайте текущие настройки, измените нужные
        элементы и передайте сюда. Операция **обратима** — повторный вызов с прежним
        списком (полученным от :meth:`object_visibilities`) восстановит исходное
        отображение; данных самого объекта она не затрагивает.

        Перед записью полезно проверить права через
        :meth:`object_check_access_rights_for_visibility` (ожидается ``"editorMode"``).

        Предусловие по id-пространству: ``object_id`` — это ``objectID``
        (F_OBJECT_ID), общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для
                которого записываются настройки видимости. Не идентификатор версии.
            settings: Список настроек видимости (:class:`VisibilitySettings`) для
                записи. Каждый элемент сериализуется через
                ``model_dump(mode="json", by_alias=True, exclude_none=True)`` в голый
                JSON-массив ``VisibilitySettingsDto`` тела запроса.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            IPSForbiddenError: При отсутствии прав на правку видимости.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.object_visibilities(102550)
                current[0].is_hidden = True
                await ips.object_update_visibility_settings(102550, current)

        Notes:
            ``operationId``: ``Visibility_UpdateVisibilitySettings``. Эндпоинт
            ``POST /core/api/objects/{objectId}/visibilities``. Тело — голый массив
            ``VisibilitySettingsDto``; ответ — void → ``None``. Связанные методы:
            :meth:`object_visibilities`,
            :meth:`object_check_access_rights_for_visibility`.
        """
        payload = [s.model_dump(mode="json", by_alias=True, exclude_none=True) for s in settings]
        await self._request(
            "post",
            f"/core/api/objects/{object_id}/visibilities",
            json=payload,
        )
        return None
