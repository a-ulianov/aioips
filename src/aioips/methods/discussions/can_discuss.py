"""Метод проверки возможности обсуждения версии объекта."""

from typing import Any

from ...core import APIManager


class CanDiscussMixin(APIManager):
    """Реализует ``GET /core/api/discussions/canDiscuss`` (``Discussions_CanDiscuss``)."""

    async def can_discuss(self: "CanDiscussMixin", object_version_id: int) -> bool:
        """Проверяет, допускает ли версия объекта ведение обсуждения.

        Лёгкая проверка перед попыткой работать с обсуждением: показывает, разрешено
        ли для данной версии объекта создавать/читать сообщения (зависит от типа объекта
        и настроек). Используйте как предусловие к чтению сообщений
        (:meth:`find_messages`) или к будущим методам записи сообщений.

        Предусловие по id-пространству (критично): аргумент — это ВЕРСИЯ объекта
        (``id`` / F_ID), а НЕ идентификатор объекта (``objectID`` / F_OBJECT_ID).
        Обсуждение привязывается именно к версии.

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта (``objectVersionId``, F_ID).
                Не идентификатор объекта.

        Returns:
            ``True``, если для данной версии объекта обсуждение допустимо; ``False``
            иначе.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.can_discuss(102550):  # 102550 = id версии, не объекта
                    messages = await ips.find_messages(102550)

        Notes:
            ``operationId``: ``Discussions_CanDiscuss``; путь
            ``GET /core/api/discussions/canDiscuss`` (query ``objectVersionId``).
            См. [[ips-object-model]] (раздел «Идентичность: объект ≠ версия»).
        """
        params: dict[str, Any] = {"objectVersionId": object_version_id}
        data = await self._request("get", "/core/api/discussions/canDiscuss", params=params)
        return bool(data)
