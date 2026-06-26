"""Метод создания нового информационного объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute, ObjectDto


class ObjectCreateMixin(APIManager):
    """Реализует ``POST /core/api/objects`` (``Objects_Create``)."""

    async def object_create(
        self: "ObjectCreateMixin",
        object_type: int,
        *,
        attributes: list[Attribute] | None = None,
        log_history: bool = True,
    ) -> ObjectDto:
        """Создаёт новый объект указанного типа в режиме создания (черновик).

        Это первый шаг двухшагового создания: метод возвращает объект в режиме создания
        (``is_creation_mode == True``) с **временным отрицательным** ``object_id``. Объект
        ещё НЕ существует в базе — его нужно зафиксировать через
        :meth:`object_commit_creation`. При неудачной фиксации временный объект
        автоматически удаляется (если ``delete_on_exception``), не оставляя мусора.

        Notes:
            Некоторые типы обязаны входить в родителя (применяемость): для них при фиксации
            нужно передать ``related_object_ids`` (см. :meth:`object_commit_creation`), иначе
            сервер вернёт ошибку. Начальные значения атрибутов можно задать сразу в
            ``attributes`` либо позже, после извлечения на редактирование.

        Args:
            object_type: Идентификатор типа создаваемого объекта (``ObjectTypeID``).
            attributes: Начальные атрибуты (список :class:`Attribute`); каждый сериализуется
                по точным ключам API. Если не задан — объект создаётся без значений.
            log_history: Журналировать ли операцию в истории модификаций.

        Returns:
            Созданная (черновая) версия объекта по схеме :class:`ObjectDto` с временным
            ``object_id`` и ``is_creation_mode == True``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import Attribute

            async with IPSClient(config=config) as ips:
                draft = await ips.object_create(
                    1116,  # тип «Комментарий»
                    attributes=[Attribute(attribute_id=10, values=["Новый объект"])],
                )
                obj_id = await ips.object_commit_creation(draft.object_id)

        References:
            ``Objects_Create``. Связанные: :meth:`object_commit_creation`, :meth:`object_delete`.
        """
        payload: dict[str, Any] = {
            "objectType": object_type,
            "attributes": [
                a.model_dump(mode="json", by_alias=True, exclude_none=True)
                for a in (attributes or [])
            ],
        }
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request("post", "/core/api/objects", json=payload, params=params)
        result = data.get("result") if isinstance(data, dict) else None
        return ObjectDto.model_validate(result)
