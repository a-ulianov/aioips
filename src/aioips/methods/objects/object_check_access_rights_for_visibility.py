"""Метод проверки прав доступа к настройкам видимости (read-check)."""

from ...core import APIManager


class ObjectCheckAccessRightsForVisibilityMixin(APIManager):
    """Реализует ``Visibility_CheckAccessRightsForVisibility`` (проверка прав на видимость)."""

    async def object_check_access_rights_for_visibility(
        self: "ObjectCheckAccessRightsForVisibilityMixin",
        version_ids: list[int],
    ) -> str:
        """Проверяет права текущего пользователя на правку настроек видимости версий.

        Возвращает агрегированный режим редактора (``EditorMode``) для набора версий:
        достаточно ли прав, чтобы открыть редактор настроек видимости, и в каком
        режиме. Это операция **только чтения** (проверка прав) — она ничего не меняет.
        Применяйте перед :meth:`object_update_visibility_settings`, чтобы заранее
        понять, разрешена ли запись настроек видимости.

        Предусловие по id-пространству: тело — список идентификаторов ВЕРСИЙ
        (``id`` / F_ID), а НЕ идентификаторов объектов (``objectID``).

        Args:
            version_ids: Список идентификаторов ВЕРСИЙ (``id`` / F_ID), для которых
                проверяются права на правку видимости. Сериализуется как голый
                JSON-массив ``list[int]`` в теле запроса.

        Returns:
            Режим редактора как строка enum ``EditorMode``: ``"none"`` (нет доступа),
            ``"readOnly"`` (только чтение) или ``"editorMode"`` (правка разрешена).
            Пустая строка, если сервер не вернул значения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                mode = await ips.object_check_access_rights_for_visibility([102550])
                if mode == "editorMode":
                    await ips.object_update_visibility_settings(102550, settings)

        Notes:
            ``operationId``: ``Visibility_CheckAccessRightsForVisibility``. Эндпоинт
            ``POST /core/api/objects/visibilities/checkAccessRights``. Тело — голый
            массив ``list[int]``; ответ — enum ``EditorMode`` (возвращается как
            строка). Связанные методы: :meth:`object_update_visibility_settings`,
            :meth:`object_visibilities`.
        """
        data = await self._request(
            "post",
            "/core/api/objects/visibilities/checkAccessRights",
            json=version_ids,
        )
        if isinstance(data, str):
            return data
        return "" if data is None else str(data)
