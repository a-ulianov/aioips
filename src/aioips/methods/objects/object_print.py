"""Метод запуска печати объекта."""

from ...core import APIManager


class ObjectPrintMixin(APIManager):
    """Реализует ``Objects_Print`` (печать объекта)."""

    async def object_print(
        self: "ObjectPrintMixin",
        object_id: int,
    ) -> None:
        """Инициирует серверную печать объекта по его связанному шаблону печати.

        Запускает на стороне сервера операцию печати объекта (по настроенному для
        его типа шаблону/правилам печати). Метод не возвращает результат печати —
        только подтверждает, что операция принята без ошибки. Применяйте, когда нужно
        программно отправить объект на печать так же, как это делает UI.

        Предусловие по id-пространству: ``object_id`` — это ``objectID``
        (F_OBJECT_ID), общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID),
                отправляемого на печать. Не идентификатор версии.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            IPSError: При ошибочном ответе сервера (например, нет шаблона печати).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_print(102550)

        Notes:
            ``operationId``: ``Objects_Print``. Эндпоинт
            ``POST /core/api/objects/{objectId}/print``. Тело пустое (``{}``);
            ответ — void → ``None``.
        """
        await self._request("post", f"/core/api/objects/{object_id}/print", json={})
        return None
