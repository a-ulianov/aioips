"""Метод получения версии объекта по правилу выбора версий."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectByVersionsRuleMixin(APIManager):
    """Реализует ``POST /core/api/objects/{id}/getObjectByVersionsRule/{ruleObjectId}``.

    Соответствует операции ``Objects_GetObjectByVersionsRule``.
    """

    async def object_by_versions_rule(
        self: "ObjectByVersionsRuleMixin",
        object_id: int,
        rule_object_id: int,
        *,
        throw_not_found: bool | None = None,
    ) -> ObjectDto:
        """Возвращает версию объекта, выбранную по заданному правилу выбора версий.

        Применяйте, когда из нескольких версий объекта нужна именно та, что отвечает
        правилу версий (``VersionsRule``) — например, актуальная версия в заданном
        контексте проекта/процесса. В отличие от :meth:`object_get` (всегда базовая
        версия по ``objectID``), результат зависит от объекта-правила
        ``rule_object_id``. Только чтение — это POST, но БЕЗ мутаций; тело не несёт
        параметров (отправляется ``{}``, чтобы IPS не вернул 415).

        Предусловие по id-пространству: ``object_id`` — это id ОБЪЕКТА
        (``objectID`` / F_OBJECT_ID), общий для версий; ``rule_object_id`` — id
        объекта-ПРАВИЛА выбора версий (``VersionsRule``), по которому выбирается
        конкретная версия.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                выбирается версия. В пути эндпоинта — ``id``.
            rule_object_id: Идентификатор объекта-правила выбора версий
                (``VersionsRule``). В пути эндпоинта — ``ruleObjectId``.
            throw_not_found: Если ``True``, при отсутствии подходящей версии сервер
                вернёт ошибку (метод поднимет исключение). ``None`` (по умолчанию) —
                query-параметр не передаётся (серверное поведение по умолчанию).

        Returns:
            Выбранная версия объекта по схеме :class:`ObjectDto`. Поля идентичности:
            ``object_id`` (объект) и ``id`` (версия); ``caption`` — заголовок.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если версия не найдена и
                ``throw_not_found`` равно ``True``).

        Example:
            async with IPSClient(config=config) as ips:
                obj = await ips.object_by_versions_rule(102550, 778)
                print(obj.object_id, obj.id, obj.caption)

        Notes:
            ``operationId``: ``Objects_GetObjectByVersionsRule``. Ответ — ``ObjectDto``
            (метод поддерживает и result-обёртку ``{entity}`` на случай расхождения со
            swagger). См. :meth:`object_get` и [[ips-object-model]] (раздел «Идентичность»).
        """
        params: dict[str, Any] = {}
        if throw_not_found is not None:
            params["throwNotFoundException"] = str(throw_not_found).lower()
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/getObjectByVersionsRule/{rule_object_id}",
            json={},
            params=params,
        )
        if isinstance(data, dict) and "entity" in data:
            data = data["entity"]
        return ObjectDto.model_validate(data)
