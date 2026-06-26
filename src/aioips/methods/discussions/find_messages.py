"""Метод поиска сообщений обсуждений по версии объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.discussions import Message


class FindMessagesMixin(APIManager):
    """Реализует ``GET /core/api/discussions/{objectVersionId}/findMessages``.

    ``operationId``: ``Discussions_FindMessages``.
    """

    async def find_messages(
        self: "FindMessagesMixin",
        object_version_id: int,
        *,
        all_object_versions: bool = False,
    ) -> list[Message]:
        """Возвращает сообщения обсуждений, относящиеся к версии объекта.

        Основной способ прочитать обсуждение конкретного объекта: отдаёт сообщения,
        привязанные к указанной версии. Флагом ``all_object_versions`` можно расширить
        выборку на сообщения всех версий объекта (всю историю обсуждений), а не только
        переданной версии. Проверить допустимость обсуждения заранее — :meth:`can_discuss`.

        Предусловие по id-пространству (критично): аргумент — это ВЕРСИЯ объекта
        (``id`` / F_ID), а НЕ идентификатор объекта (``objectID`` / F_OBJECT_ID).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта (``objectVersionId``, F_ID),
                для которой ищутся сообщения.
            all_object_versions: Если ``True`` — вернуть сообщения по всем версиям
                объекта; если ``False`` (по умолчанию) — только по указанной версии.

        Returns:
            Список сообщений по схеме :class:`Message`. Пустой список означает, что у
            версии объекта нет сообщений обсуждения.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                # все сообщения обсуждения по всей истории версий объекта
                messages = await ips.find_messages(102550, all_object_versions=True)

        Notes:
            ``operationId``: ``Discussions_FindMessages``; путь
            ``GET /core/api/discussions/{objectVersionId}/findMessages``
            (query ``allObjectVersions``, массив ``MessageDto``).
            См. объектной модели IPS (раздел «Идентичность: объект ≠ версия»).
        """
        params: dict[str, Any] = {"allObjectVersions": str(all_object_versions).lower()}
        path = f"/core/api/discussions/{object_version_id}/findMessages"
        data = await self._request("get", path, params=params)
        return [Message.model_validate(item) for item in data]
