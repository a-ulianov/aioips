"""Метод создания информационного объекта по прототипу."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import CreateObjectByPrototype


class ObjectCreateByPrototypeMixin(APIManager):
    """Реализует ``POST /core/api/objects/CreateByPrototype`` (``Objects_CreateByPrototype``)."""

    async def object_create_by_prototype(
        self: "ObjectCreateByPrototypeMixin",
        prototype: CreateObjectByPrototype,
        *,
        log_history: bool = True,
    ) -> dict[str, Any]:
        """Создаёт объект по прототипу (объекту-образцу) и возвращает черновик с потомками.

        Прототип задаёт тип и применимые атрибуты нового объекта (см.
        :class:`~aioips.schemas.objects.CreateObjectByPrototype`). Объект создаётся в
        режиме создания (черновик с временным отрицательным id) — он ещё НЕ существует в
        базе и должен быть зафиксирован через :meth:`object_commit_creation`. В отличие от
        :meth:`object_create`, тип не задаётся явно, а наследуется от прототипа, и сервер
        дополнительно возвращает идентификаторы связанных (дочерних) объектов, которые
        нужно учесть при фиксации (применяемость).

        Предусловие по id-пространству: ``prototype.prototype_id`` — идентификатор ОБЪЕКТА
        (или версии) прототипа, по которому копируется структура.

        Args:
            prototype: Параметры создания по прототипу (:class:`CreateObjectByPrototype`):
                обязательный ``prototype_id`` и необязательные ``is_article``,
                ``context_rule``, ``current_project``. Сериализуется в тело запроса.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            «Сырой» словарь ответа ``ObjectCreatedByPrototypeDto`` с полями
            ``objectDto`` (созданная черновая версия) и ``relatedObjectIds`` (список
            id связанных объектов). Структура не типизирована намеренно (опаковый DTO).
            Пустой словарь, если сервер не вернул результат.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import CreateObjectByPrototype

            async with IPSClient(config=config) as ips:
                created = await ips.object_create_by_prototype(
                    CreateObjectByPrototype(prototype_id=102550, is_article=True)
                )
                draft = created["objectDto"]
                related = created["relatedObjectIds"]

        References:
            ``Objects_CreateByPrototype``. Связанные: :meth:`object_create`,
            :meth:`object_commit_creation`.
        """
        payload = prototype.model_dump(mode="json", by_alias=True, exclude_none=True)
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post", "/core/api/objects/CreateByPrototype", json=payload, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        return result if isinstance(result, dict) else {}
