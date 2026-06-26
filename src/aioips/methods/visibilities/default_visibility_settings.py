"""Метод получения дефолтных настроек видимости объектов."""

from ...core import APIManager
from ...schemas.visibilities import VisibilitySettings


class DefaultVisibilitySettingsMixin(APIManager):
    """Реализует ``GET /api/visibilities/getDefault``.

    operationId ``Visibility_GetDefaultVisibilitySettings``.
    """

    async def default_visibility_settings(
        self: "DefaultVisibilitySettingsMixin",
    ) -> list[VisibilitySettings]:
        """Возвращает список дефолтных настроек видимости объектов IPS.

        Дефолтные настройки видимости определяют, какие объекты (узлы) по умолчанию
        показаны или скрыты в интерфейсе и какой значок им сопоставлен. Метод отдаёт
        полный набор таких настроек «из коробки» (без учёта персональных переопределений).

        Когда применять: чтобы прочитать базовую конфигурацию видимости — например, для
        отображения или сравнения с пользовательскими настройками. Предусловий нет.

        Returns:
            Список настроек по схеме :class:`VisibilitySettings`. Значимые поля:
            ``object_id`` / ``object_type`` (идентичность), ``is_visible`` / ``is_hidden``
            (показан/скрыт), ``icon`` (значок). Пустой список означает отсутствие
            дефолтных настроек видимости.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.default_visibility_settings()
                hidden = [s.object_name for s in settings if s.is_hidden]

        Notes:
            operationId ``Visibility_GetDefaultVisibilitySettings``; путь
            ``GET /api/visibilities/getDefault`` (массив ``VisibilitySettingsDto``).
        """
        data = await self._request("get", "/api/visibilities/getDefault")
        return [VisibilitySettings.model_validate(item) for item in data]
