"""Метод фиксации создания объекта."""

from typing import Any

from ...core import APIManager


class ObjectCommitCreationMixin(APIManager):
    """Реализует ``.../objects/{objectId}/commitCreation`` (``Objects_CommitCreation``)."""

    async def object_commit_creation(
        self: "ObjectCommitCreationMixin",
        object_id: int,
        *,
        delete_on_exception: bool = True,
        auto_checkout: bool = False,
        related_object_ids: list[int] | None = None,
        log_history: bool = True,
    ) -> int:
        """Фиксирует создание черновика объекта и возвращает его постоянный идентификатор.

        Завершает создание, начатое :meth:`object_create`: переводит черновик (с временным
        отрицательным id) в постоянный объект базы. Возвращает **новый положительный**
        ``objectID``, по которому объект далее доступен (``object_get`` и пр.).

        Для типов с обязательной применяемостью (объект должен входить в родителя) укажите
        родителя в ``related_object_ids`` — иначе сервер вернёт ошибку «должен обязательно
        входить в один из объектов типов …».

        Args:
            object_id: Временный идентификатор черновика (из :meth:`object_create`).
            delete_on_exception: При ошибке фиксации удалить черновик (не оставлять мусор).
            auto_checkout: Оставить объект извлечённым на редактирование после создания.
            related_object_ids: Идентификаторы родительских объектов, в состав которых
                включается создаваемый объект (нужно для типов с обязательным родителем).
            log_history: Журналировать ли операцию в истории модификаций.

        Returns:
            Постоянный идентификатор созданного объекта (``objectID``).

        Raises:
            IPSError: При ошибочном ответе сервера (например, нарушение применяемости).

        Example:
            async with IPSClient(config=config) as ips:
                draft = await ips.object_create(1116)
                object_id = await ips.object_commit_creation(draft.object_id)

        References:
            ``Objects_CommitCreation``. Связанные: :meth:`object_create`, :meth:`object_check_out`.
        """
        payload: dict[str, Any] = {
            "deleteOnException": delete_on_exception,
            "autoCheckout": auto_checkout,
            "relatedObjectIds": related_object_ids or [],
        }
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/commitCreation", json=payload, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        new_id = result.get("objectId") if isinstance(result, dict) else None
        return int(new_id) if new_id is not None else 0
