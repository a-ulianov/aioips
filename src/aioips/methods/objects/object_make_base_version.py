"""Метод назначения версии объекта базовой."""

from ...core import APIManager


class ObjectMakeBaseVersionMixin(APIManager):
    """Реализует ``.../objects/{objectId}/makeBaseVersion`` (``Objects_MakeBaseVersion``)."""

    async def object_make_base_version(
        self: "ObjectMakeBaseVersionMixin",
        object_id: int,
    ) -> None:
        """Делает указанную версию объекта базовой (МУТИРУЮЩАЯ операция).

        Назначает переданную версию объекта базовой (актуальной): после этого именно она
        используется по умолчанию при разрешении версий. Для пакетной обработки нескольких
        объектов используйте :meth:`object_make_base_versions`.

        Args:
            object_id: Идентификатор ВЕРСИИ объекта, назначаемой базовой (``ID`` версии,
                не ``ObjectID``).

        Returns:
            ``None`` — метод ничего не возвращает (тип ответа ``void``); базовая версия
            меняется как побочный эффект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_make_base_version(33001)

        References:
            ``Objects_MakeBaseVersion``. Связанные: :meth:`object_make_base_versions`,
            :meth:`object_base_version`.
        """
        await self._request("post", f"/core/api/objects/{object_id}/makeBaseVersion", json={})
        return None
