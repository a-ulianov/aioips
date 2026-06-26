"""Метод получения настроек видимости объекта."""

from ...core import APIManager
from ...schemas.visibilities import VisibilitySettings


class ObjectVisibilitiesMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/visibilities``.

    Соответствует операции ``Visibility_GetVisibilitySettings``.
    """

    async def object_visibilities(
        self: "ObjectVisibilitiesMixin",
        object_id: int,
    ) -> list[VisibilitySettings]:
        """Возвращает настройки видимости объекта (как он отображается в дереве/UI).

        Видимость задаёт, какие связанные объекты (узлы) показываются или скрыты в
        интерфейсе для данного объекта и какие значки им сопоставлены. Метод возвращает
        список настроек видимости для объекта. Применяйте для построения/анализа
        отображения состава объекта в UI. Перед чтением полезно убедиться, что видимость
        в принципе доступна для объекта, через
        :meth:`object_check_visibility_available`. Только чтение.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                запрашиваются настройки видимости. Не идентификатор версии (``id`` / F_ID).

        Returns:
            Список :class:`VisibilitySettings` (возможно пустой). Значимые поля элемента:
            ``object_id``, ``object_type``, ``object_name``, ``is_visible``,
            ``is_hidden``, ``icon``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.object_visibilities(102550)
                for s in settings:
                    print(s.object_name, s.is_visible)

        Notes:
            ``operationId``: ``Visibility_GetVisibilitySettings``. Ответ — голый массив
            ``VisibilitySettingsDto``, не result-обёртка. Связано с
            :meth:`object_check_visibility_available`.
        """
        data = await self._request("get", f"/core/api/objects/{object_id}/visibilities")
        if not isinstance(data, list):
            return []
        return [VisibilitySettings.model_validate(item) for item in data]
