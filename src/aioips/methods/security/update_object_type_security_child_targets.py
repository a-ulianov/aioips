"""Метод обновления прав дочерних целей безопасности типа объекта (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.security import Security


class UpdateObjectTypeSecurityChildTargetsMixin(APIManager):
    """Реализует обновление прав дочерних целей безопасности типа объекта.

    Путь ``POST``:
    ``.../security/objectTypes/{objectTypeId}/childTargets``
    operationId ``Security_UpdateObjectTypeSecurityChildTargets``.
    """

    async def update_object_type_security_child_targets(
        self: "UpdateObjectTypeSecurityChildTargetsMixin",
        object_type_id: int,
        body: Security | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает права для ДОЧЕРНИХ целей безопасности ТИПА объекта (МУТАЦИЯ).

        УСТАНОВКА прав (перезапись): распространяет/обновляет настройки безопасности
        для дочерних целей (наследников) указанного типа объекта. Это опасная операция —
        она меняет реальные права доступа в системе, а не читает их. Тело — снимок прав
        :class:`Security` (``SecurityDto``): передаётся желаемое итоговое состояние.

        Когда применять: чтобы применить/выровнять права наследуемых целей по типу объекта.
        Парный read для получения текущего снимка — :meth:`object_type_security`.

        Обратимость: операция ОБРАТИМА по схеме write-same-back. Перед записью прочитайте
        текущее состояние парным :meth:`object_type_security` и сохраните его; для отката
        запишите тот же снимок обратно этим методом. Тест отката: прочитать → записать тот
        же объект обратно — состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            object_type_id: Идентификатор ТИПА объекта (метаданное «тип объекта»), не
                объекта/версии.
            body: Снимок прав (:class:`Security` или эквивалентный ``dict``,
                ``SecurityDto``). Для точного round-trip передавайте «сырой» результат
                парного read :meth:`object_type_security`. Модель сериализуется
                ``by_alias`` + ``exclude_none``; ``dict`` уходит как есть.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 403 при недостатке прав; 404,
                если тип не найден).

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.object_type_security(1031)  # бэкап
                await ips.update_object_type_security_child_targets(1031, current, confirm=True)

        Notes:
            operationId ``Security_UpdateObjectTypeSecurityChildTargets``; тело —
            ``SecurityDto``. Путь ``POST``:
            ``.../security/objectTypes/{objectTypeId}/childTargets``.
            Парный read — :meth:`object_type_security`.
        """
        if confirm is not True:
            raise ValueError(
                "update_object_type_security_child_targets меняет права доступа; "
                "передайте confirm=True",
            )
        payload = (
            body.model_dump(mode="json", by_alias=True, exclude_none=True)
            if isinstance(body, Security)
            else body
        )
        await self._request(
            "post",
            f"/core/api/security/objectTypes/{object_type_id}/childTargets",
            json=payload,
        )
        return None
