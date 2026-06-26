"""Метод удаления атрибута связи (мутирующий, разрушающий — защищён confirm-гейтом)."""

from typing import Any

from ...core import APIManager


class RelationDeleteAttributeMixin(APIManager):
    """Реализует ``DELETE /core/api/relations/{relationId}/attributes/{attributeId}``.

    ``operationId``: ``RelationAttributes_DeleteAttribute``.
    """

    async def relation_delete_attribute(
        self: "RelationDeleteAttributeMixin",
        relation_id: int,
        attribute_id: int,
        *,
        confirm: bool = False,
        log_history: bool = True,
    ) -> None:
        """Удаляет один атрибут СВЯЗИ по id связи и id атрибута (РАЗРУШАЮЩАЯ, ``confirm``).

        Связь в IPS — атрибутируемая сущность; у неё есть собственные атрибуты (например,
        позиционное обозначение или количество в составе). Этот метод удаляет ОДИН такой
        атрибут связи. Операция необратима, поэтому по умолчанию НЕ выполняется: требуется
        явный ``confirm=True``, иначе поднимается :class:`ValueError` ещё до обращения к
        серверу. Удаляется атрибут связи, а не сама связь (для этого — :meth:`relation_delete`)
        и не атрибут объекта-конца.

        ПРЕДУСЛОВИЕ: объект-РОДИТЕЛЬ связи должен быть в режиме, разрешающем правку на
        текущем шаге ЖЦ (как правило — извлечён на редактирование, checkout). Внимание:
        ``relation_id`` нестабилен (меняется при checkout/checkin родителя) — используйте
        свежий идентификатор.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, путь ``{relationId}``;
                отдельное id-пространство связей, нестабилен — не кэшируйте).
            attribute_id: Идентификатор ТИПА атрибута связи к удалению (``attributeID``,
                путь ``{attributeId}``).
            confirm: Подтверждение разрушающей операции. Без ``True`` метод не делает
                запрос и поднимает :class:`ValueError`.
            log_history: Если ``True`` (по умолчанию), сервер логирует историю
                модификаций (query ``isNeedToLogModificationHistory``); ``False`` — без
                журналирования.

        Returns:
            ``None``. Ответ-обёртка ``Nothing*`` не несёт полезной нагрузки; успех —
            отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибке сервера (в т.ч. если родитель связи не извлечён на
                редактирование или атрибут отсутствует).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.relation_delete_attribute(700123, 205, confirm=True)

        Notes:
            ``operationId``: ``RelationAttributes_DeleteAttribute``. Связанные:
            :meth:`relation_set_attributes`, :meth:`relation_delete`. Тело DELETE — ``{}``
            (на случай требования сервером ``Content-Type``). См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Удаление атрибута связи необратимо: передайте confirm=True для подтверждения"
            )
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request(
            "delete",
            f"/core/api/relations/{relation_id}/attributes/{attribute_id}",
            json={},
            params=params,
        )
        return None
