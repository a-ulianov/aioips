"""Метод получения списка форм, применимых к версии объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import QuickObjectInfo


class FormsForMixin(APIManager):
    """Реализует ``GET /core/api/forms/{versionId}/formsFor`` (``Forms_GetFormsFor``)."""

    async def forms_for(
        self: "FormsForMixin",
        version_id: int,
        *,
        is_create_object: bool | None = None,
        is_relation: bool | None = None,
    ) -> list[QuickObjectInfo]:
        """Возвращает список форм, применимых к указанной версии объекта.

        Для данной версии объекта подбирается перечень подходящих форм (как кратких
        сведений об объектах-формах). Флаги уточняют контекст: подбор для создания
        объекта и/или для связи.

        Предусловие по id-пространству (критично): аргумент — идентификатор ВЕРСИИ
        (``versionId`` / F_ID), а НЕ идентификатор объекта (``objectID``).

        Когда применять: чтобы узнать, какие формы доступны для версии (например, при
        открытии карточки объекта). Загрузить конкретную форму по её версии — :meth:`form`.

        Args:
            version_id: Идентификатор ВЕРСИИ объекта (``versionId`` / F_ID), для которой
                подбираются формы. Не идентификатор объекта.
            is_create_object: Если задано — подбирать формы для сценария создания
                объекта (query ``isCreateObject``). ``None`` — параметр не передаётся.
            is_relation: Если задано — подбирать формы для сценария связи
                (query ``isRelation``). ``None`` — параметр не передаётся.

        Returns:
            Список кратких сведений о формах по схеме :class:`QuickObjectInfo`. Пустой
            список означает отсутствие применимых форм.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                forms = await ips.forms_for(102551)
                for f in forms:
                    print(f.id, f.caption)

        Notes:
            operationId ``Forms_GetFormsFor``; путь
            ``GET /core/api/forms/{versionId}/formsFor`` (необязательные query
            ``isCreateObject``, ``isRelation``); ответ — массив ``QuickObjectInfoDto``.
            Внимание: путь с сегментом ``/formsFor`` — иной эндпоинт, чем
            ``/{versionId}`` (см. :meth:`form`).
        """
        params: dict[str, Any] = {}
        if is_create_object is not None:
            params["isCreateObject"] = str(is_create_object).lower()
        if is_relation is not None:
            params["isRelation"] = str(is_relation).lower()
        data = await self._request(
            "get",
            f"/core/api/forms/{version_id}/formsFor",
            params=params or None,
        )
        return [QuickObjectInfo.model_validate(item) for item in data]
