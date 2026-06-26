"""Общая основа методов расширенного поиска связей (read-only POST).

Все четыре метода (``consist_from`` / ``enters_in`` / ``enters_in_version`` / ``select``)
шлют POST со сложным телом и разбирают голый массив ``RelationSelectResultDto``. Общая
логика вынесена сюда, чтобы не дублировать сериализацию и разбор (DRY).
"""

from ...core import APIManager
from ...schemas.relations import (
    ObjectRelationsSelectParameters,
    RelationSelectResult,
    RelationsSelectParameters,
)

_SelectParams = ObjectRelationsSelectParameters | RelationsSelectParameters


class _ExtendedRelationSelectBase(APIManager):
    """Базовый mixin: POST со схемой параметров → ``list[RelationSelectResult]``."""

    async def _post_relation_select(
        self: "_ExtendedRelationSelectBase",
        endpoint: str,
        params: _SelectParams,
    ) -> list[RelationSelectResult]:
        """Шлёт POST с телом ``params`` и разбирает массив ``RelationSelectResultDto``.

        Args:
            endpoint: Путь эндпоинта (``/core/api/relations/...``).
            params: Параметры поиска (схема параметров расширенного поиска связей).

        Returns:
            Список найденных связей по схеме :class:`RelationSelectResult` (пустой, если
            ничего не найдено).

        Raises:
            IPSError: При ошибочном ответе сервера.
        """
        payload = params.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", endpoint, json=payload)
        return [RelationSelectResult.model_validate(item) for item in (data or [])]
