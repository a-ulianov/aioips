"""Метод получения отображаемого представления сущности метаданных по GUID."""

from typing import Any
from uuid import UUID

from ...core import APIManager


class DisplayableByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/displayable/byGuid/{guid}``."""

    async def displayable_by_guid(
        self: "DisplayableByGuidMixin",
        guid: UUID | str,
    ) -> dict[str, Any] | None:
        """Возвращает «отображаемое» (человекочитаемое) представление сущности по GUID.

        В метаданных IPS многие сущности реализуют интерфейс ``IDisplayable`` — они умеют
        отдавать строку для показа в интерфейсе. Метод по GUID любой такой сущности
        метаданных (тип объекта, тип атрибута, схема/уровень/шаг ЖЦ и т.п.) возвращает её
        DTO ``ImsDisplayableDto`` с полем ``text`` — готовой подписью. Ответ обёрнут в
        ``ImsDisplayableDtoNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь — наружу отдаётся «сырой» DTO (как ``dict``) либо ``None``.

        Тело DTO простое (``{"text": "..."}``), поэтому возвращается ``dict`` без
        выделенной pydantic-схемы — чтобы не плодить тривиальную модель.

        Когда применять: чтобы получить подпись сущности метаданных для UI/лога, имея
        только её GUID, без знания конкретного типа сущности. Чтобы узнать сам ТИП
        сущности по GUID (тип объекта/атрибута/ЖЦ-сущность) — :meth:`globals_by_guid`.

        Args:
            guid: GUID сущности метаданных (``ObjectType.guid`` / ``AttributeType.guid`` /
                guid схемы/уровня/шага ЖЦ и т.п.). Подставляется в URL как есть
                (``UUID`` или строка).

        Returns:
            Словарь с DTO ``ImsDisplayableDto`` (ключ ``text`` — строка для показа) либо
            ``None``, если сущность с таким GUID не найдена (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                view = await ips.displayable_by_guid("cad001c5-306c-11d8-b4e9-00304f19f545")
                if view is not None:
                    print(view.get("text"))

        Notes:
            operationId ``Metadata_GetDisplayableByGuid``; путь
            ``GET /core/api/metadata/displayable/byGuid/{guid}``
            (``ImsDisplayableDtoNullableResultDto``). Связанный метод —
            :meth:`globals_by_guid` (вид сущности по GUID).
        """
        data = await self._request("get", f"/core/api/metadata/displayable/byGuid/{guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return dict(entity) if isinstance(entity, dict) else None
