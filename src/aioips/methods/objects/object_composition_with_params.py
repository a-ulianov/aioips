"""Метод получения состава объекта по параметрам фильтрации."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectCompositionWithParamsMixin(APIManager):
    """Реализует ``POST /core/api/objects/{projectVersionId}/compositionWithParams``.

    Соответствует операции ``Objects_GetObjectCompositionWithParams``.
    """

    async def object_composition_with_params(
        self: "ObjectCompositionWithParamsMixin",
        object_id: int,
        *,
        relation_type_id: int = 0,
        part_type_ids: list[int] | None = None,
    ) -> list[ObjectDto]:
        """Возвращает состав объекта — его дочерние объекты по связи заданного типа.

        Применяйте для структурных связей «родитель → потомки» (например, состав
        изделия, вложения сборки). Состав — это дочерние объекты, связанные с
        родителем связью типа ``relation_type_id``. Чтобы результат не был пустым, как
        правило, необходимо указать ``part_type_ids`` — типы дочерних объектов, которые
        нужно вернуть: без них сервер обычно отдаёт пустой список (см. граблям).

        Важно (что НЕ является составом): архивная принадлежность документа задаётся
        атрибутом-ссылкой (``ftObjectLink``, атрибут «Архив» = id 1029), а НЕ составом,
        поэтому через этот метод она НЕ извлекается — для неё используйте
        :meth:`objects_select` с ``content=ID``.

        Сервер возвращает элементы ``ObjectCompositionDto`` с полями ``object``
        (дочерний объект) и ``relation`` (связь). Метод извлекает только
        ``object`` и валидирует его как :class:`ObjectDto`; данные связи
        не возвращаются.

        Args:
            object_id: Идентификатор объекта-родителя (``objectID`` / F_OBJECT_ID;
                в пути эндпоинта — ``projectVersionId``), состав которого запрашивается.
            relation_type_id: Идентификатор типа связи между родителем и
                дочерними объектами. По умолчанию ``0`` (без фильтра по типу связи).
            part_type_ids: Идентификаторы типов дочерних объектов, которые нужно
                вернуть. Если не задан, в тело запроса уходит пустой список
                ``[]`` (передавать ``null`` нельзя — сервер отвечает 500).

        Returns:
            Список дочерних объектов состава по схеме :class:`ObjectDto`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parts = await ips.object_composition_with_params(
                    102550,
                    relation_type_id=4,
                    part_type_ids=[1127],
                )
                for part in parts:
                    print(part.object_id, part.caption)

        References:
            ``Objects_GetObjectCompositionWithParams``.
        """
        payload: dict[str, Any] = {
            "relationTypeId": relation_type_id,
            "partTypeIds": part_type_ids if part_type_ids is not None else [],
        }
        data = await self._request(
            "post", f"/core/api/objects/{object_id}/compositionWithParams", json=payload
        )
        items = data if isinstance(data, list) else []
        result: list[ObjectDto] = []
        for item in items:
            obj = item.get("object") if isinstance(item, dict) else None
            if obj is not None:
                result.append(ObjectDto.model_validate(obj))
        return result
