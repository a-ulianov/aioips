"""Метод исключения объектов из состава по идентификаторам связей."""

from typing import Any

from ...core import APIManager


class ObjectExcludeFromCompositionMixin(APIManager):
    """Реализует ``.../excludeFromComposition`` (``Objects_ExcludeFromComposition``)."""

    async def object_exclude_from_composition(
        self: "ObjectExcludeFromCompositionMixin",
        relation_ids: list[int],
        *,
        confirm: bool = False,
        delete_relation_mode: int | None = None,
        log_history: bool = True,
        ignore_exceptions: bool | None = None,
    ) -> list[int]:
        """Исключает объекты из состава по id связей (РАЗРУШАЮЩАЯ операция, гейт ``confirm``).

        Удаляет связи «родитель → потомок» в составе изделия, заданные идентификаторами
        связей (``RelationID``), тем самым исключая дочерние версии из состава. Операция
        необратима (удаляет связи), поэтому по умолчанию НЕ выполняется: требуется явный
        ``confirm=True``, иначе поднимается :class:`ValueError` ещё до обращения к серверу.

        Предусловие: версия-проект, из состава которой исключаются потомки, обычно должна
        быть в режиме редактирования (см. :meth:`object_check_out` / :meth:`object_edit`).
        Внимание: ``RelationID`` нестабилен между запросами — получайте свежие id состава
        (см. :meth:`object_composition_with_params`) перед исключением, не кэшируйте.

        Args:
            relation_ids: Идентификаторы связей состава (``RelationID``), подлежащих
                удалению. Передаются телом запроса в поле ``relationIds``.
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError`.
            delete_relation_mode: Режим удаления связи (``deleteRelationMode``); ``None`` —
                поле в тело не передаётся (серверный режим по умолчанию).
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).
            ignore_exceptions: Если задано, управляет игнорированием ошибок по элементам
                (query ``isNeedToIgnoreExceptions``); ``None`` — параметр не передаётся.

        Returns:
            Список id успешно исключённых элементов (``list[int]``); пустой список, если
            сервер ничего не вернул.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSConflictError: Если версия-проект не в режиме редактирования либо связь
                нельзя удалить.
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                removed = await ips.object_exclude_from_composition(
                    [55001, 55002], confirm=True
                )

        References:
            ``Objects_ExcludeFromComposition``. Связанные: :meth:`object_include_in_composition`,
            :meth:`object_composition_with_params`.
        """
        if confirm is not True:
            raise ValueError(
                "Исключение из состава необратимо: передайте confirm=True для подтверждения"
            )
        payload: dict[str, Any] = {"relationIds": relation_ids}
        if delete_relation_mode is not None:
            payload["deleteRelationMode"] = delete_relation_mode
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        if ignore_exceptions is not None:
            params["isNeedToIgnoreExceptions"] = str(ignore_exceptions).lower()
        data = await self._request(
            "post",
            "/core/api/objects/excludeFromComposition",
            json=payload,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return [int(x) for x in (result or [])]
