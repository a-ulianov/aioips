"""Метод удаления объекта."""

from typing import Any

from ...core import APIManager


class ObjectDeleteMixin(APIManager):
    """Реализует ``POST /core/api/objects/{objectId}/delete`` (``Objects_Delete``)."""

    async def object_delete(
        self: "ObjectDeleteMixin",
        object_id: int,
        *,
        confirm: bool = False,
        delete_mode: int = 0,
        log_history: bool = True,
    ) -> int:
        """Удаляет объект (РАЗРУШАЮЩАЯ операция, защищена параметром ``confirm``).

        Удаляет объект из базы. Поскольку операция необратима, по умолчанию НЕ выполняется:
        требуется явный ``confirm=True``, иначе поднимается :class:`ValueError` ещё до
        обращения к серверу. Перед удалением рекомендуется проверить зависимости (объект
        может входить в состав/быть связанным).

        Args:
            object_id: Идентификатор удаляемого объекта (``objectID``).
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает запрос.
            delete_mode: Режим удаления/каскада (``0`` — обычный). См. ``Consts.DeleteInstances``.
            log_history: Журналировать ли операцию в истории модификаций.

        Returns:
            Код результата удаления (``0`` — успех).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSConflictError: Если объект нельзя удалить (есть зависимости/блокировка).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_delete(102550, confirm=True)

        References:
            ``Objects_Delete``. Связанные: :meth:`object_create`, :meth:`object_commit_creation`.
        """
        if confirm is not True:
            raise ValueError(
                "Удаление объекта необратимо: передайте confirm=True для подтверждения"
            )
        params: dict[str, Any] = {
            "deleteMode": str(delete_mode),
            "isNeedToLogModificationHistory": str(log_history).lower(),
        }
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/delete", json={}, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return int(result) if isinstance(result, int) else 0
