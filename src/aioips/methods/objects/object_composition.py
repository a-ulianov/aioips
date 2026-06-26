"""Метод получения состава объекта по версии проекта с правилом контекста."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectCompositionParams, ObjectDto


class ObjectCompositionMixin(APIManager):
    """Реализует ``POST /core/api/objects/{projectVersionId}/composition``.

    Соответствует операции ``Objects_GetObjectComposition``.
    """

    async def object_composition(
        self: "ObjectCompositionMixin",
        project_version_id: int,
        *,
        context_rule: dict[str, Any] | None = None,
    ) -> list[ObjectDto]:
        """Возвращает состав объекта по версии проекта с учётом правила контекста.

        Применяйте для структурных связей «родитель → потомки» (состав изделия,
        вложения сборки), когда нужен простой запрос состава с необязательным
        правилом контекста версий. В отличие от :meth:`object_composition_with_params` (фильтрация
        по типу связи и типам потомков), здесь набор задаётся версией проекта и
        контекстом версий. Только чтение — это POST, но БЕЗ мутаций.

        Предусловие по id-пространству (важно): ``project_version_id`` в пути — это id
        ВЕРСИИ (F_ID / ``id``), от которой берётся состав, а НЕ id объекта
        (``objectID`` / F_OBJECT_ID). Правило контекста ``context_rule`` влияет на то,
        какие версии дочерних объектов попадут в результат.

        Args:
            project_version_id: Идентификатор ВЕРСИИ проекта (F_ID / ``id``), состав
                которой запрашивается. В пути эндпоинта — ``projectVersionId``.
            context_rule: Правило контекста версий (исходный ``ContextRuleDto``) как
                словарь ``{"versionRuleObjectId": ..., "editingContextId": ...,
                "editingContextMode": ...}``. Если ``None`` (по умолчанию), в тело
                уходит пустой объект ``{}`` (контекст по умолчанию).

        Returns:
            Список дочерних объектов состава по схеме :class:`ObjectDto` (пустой
            список, если состав пуст). Метод извлекает поле ``object`` каждого
            элемента ``ObjectCompositionDto``; данные связи не возвращаются.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                parts = await ips.object_composition(102550)
                for part in parts:
                    print(part.object_id, part.caption)

        Notes:
            ``operationId``: ``Objects_GetObjectComposition``. Тело — ``ObjectCompositionParamsDto``
            (или ``{}`` если контекст не задан; POST IPS требует тело, иначе 415).
            Ответ — «голый» массив ``ObjectCompositionDto`` с полями ``object`` и
            ``relation``. См. :meth:`object_composition_with_params` и объектной модели IPS
            (раздел «Состав»).
        """
        params = ObjectCompositionParams(context_rule=context_rule)
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", f"/core/api/objects/{project_version_id}/composition", json=payload
        )
        items = data if isinstance(data, list) else []
        result: list[ObjectDto] = []
        for item in items:
            obj = item.get("object") if isinstance(item, dict) else None
            if obj is not None:
                result.append(ObjectDto.model_validate(obj))
        return result
