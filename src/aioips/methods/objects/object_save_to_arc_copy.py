"""Метод сохранения объекта в архивную копию."""

from typing import Any

from ...core import APIManager


class ObjectSaveToArcCopyMixin(APIManager):
    """Реализует ``Objects_SaveToArcCopy`` (сохранение объекта в архивную копию)."""

    async def object_save_to_arc_copy(
        self: "ObjectSaveToArcCopyMixin",
        object_id: int,
        *,
        log_history: bool = True,
    ) -> None:
        """Сохраняет объект в архивную копию средствами сервера.

        Запускает серверную операцию формирования архивной копии объекта (снимок его
        файлов/состояния в архивное хранилище). Метод не возвращает содержимое копии —
        тип ответа ``Nothing`` (пустой результат), поэтому возвращается ``None``;
        успех = отсутствие ошибки. Применяйте для программного архивирования объекта.

        Предусловие по id-пространству: ``object_id`` — это ``objectID``
        (F_OBJECT_ID), общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID),
                сохраняемого в архивную копию. Не идентификатор версии.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            ``None``. Ответ — ``NothingProcessResultWithLogInfoDto`` с пустым
            ``result`` (``Nothing``): значимых данных нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_save_to_arc_copy(102550)

        Notes:
            ``operationId``: ``Objects_SaveToArcCopy``. Эндпоинт
            ``POST /core/api/objects/{objectId}/saveToArcCopy``. Тело пустое (``{}``);
            ответ — ``NothingProcessResultWithLogInfoDto`` (``result`` распаковывается
            в ``None``). Связанный метод: :meth:`object_save_to_disk`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request(
            "post",
            f"/core/api/objects/{object_id}/saveToArcCopy",
            json={},
            params=params,
        )
        return None
