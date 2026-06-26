"""Метод проверки доступности настроек видимости для объекта."""

from ...core import APIManager


class ObjectCheckVisibilityAvailableMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/visibilities/checkVisibilityAvailable``.

    Соответствует операции ``Visibility_CheckVisibilityAvailableForObject``.
    """

    async def object_check_visibility_available(
        self: "ObjectCheckVisibilityAvailableMixin",
        object_id: int,
    ) -> bool:
        """Проверяет, доступны ли настройки видимости для объекта.

        Быстрая проверка-гейт перед чтением видимости: отвечает, поддерживает ли объект
        настройки видимости вообще (не для всех типов/состояний объектов они применимы).
        Вызывайте перед :meth:`object_visibilities`, чтобы не запрашивать настройки там,
        где их быть не может. Только чтение.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                проверяется доступность видимости. Не идентификатор версии (``id`` / F_ID).

        Returns:
            ``True``, если настройки видимости доступны для объекта; иначе ``False``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_check_visibility_available(102550):
                    settings = await ips.object_visibilities(102550)

        Notes:
            ``operationId``: ``Visibility_CheckVisibilityAvailableForObject``. Ответ —
            голое булево (``type: boolean``), не result-обёртка. Связано с
            :meth:`object_visibilities`.
        """
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/visibilities/checkVisibilityAvailable"
        )
        return bool(data)
