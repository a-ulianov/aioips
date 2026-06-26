"""Метод получения ролевых режимов отображения таблиц IMBASE."""

from ...core import APIManager
from ...schemas.imbase import RoleDisplayModeOption


class ImBaseRoleDisplayModeOptionsMixin(APIManager):
    """Реализует ``GET /core/api/imbase/roleDisplayModeOptions``."""

    async def imbase_role_display_mode_options(
        self: "ImBaseRoleDisplayModeOptionsMixin",
    ) -> list[RoleDisplayModeOption]:
        """Возвращает ролевые режимы отображения таблиц IMBASE.

        Отдаёт список ролей, для которых настроен индивидуальный режим отображения
        таблиц IMBASE, с их названиями и идентификаторами. Применяется при построении
        переключателя режима «по роли».

        Когда применять: для UI выбора ролевого режима отображения IMBASE. Общие
        режимы (общий/персональный/по роли) — :meth:`imbase_display_mode_options`. Те
        же данные входят в сводный снимок :meth:`imbase_client_cache_state` (поле
        ``role_display_mode_options``, там — «сырые» словари). Ответ — голый массив,
        без result-обёртки.

        Returns:
            Список ролей по схеме :class:`RoleDisplayModeOption` (``object_id`` —
            GUID роли, ``object_version_id`` — id версии, ``name`` — название). Пустой
            список означает отсутствие ролевых настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                roles = await ips.imbase_role_display_mode_options()
                for role in roles:
                    print(role.name, role.object_id)

        Notes:
            operationId ``ImBase_GetRoleDisplayModeOptions``; путь
            ``GET /core/api/imbase/roleDisplayModeOptions`` (массив
            ``RoleDisplayModeOptionDto``).
        """
        data = await self._request("get", "/core/api/imbase/roleDisplayModeOptions")
        items = data if isinstance(data, list) else []
        return [RoleDisplayModeOption.model_validate(item) for item in items]
