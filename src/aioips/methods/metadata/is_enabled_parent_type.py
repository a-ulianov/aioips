"""Метод проверки, разрешён ли тип объекта как родитель по спискам типов."""

from typing import Any

from ...core import APIManager


class IsEnabledParentTypeMixin(APIManager):
    """Реализует ``POST .../applicabilities/isEnabledParentType/{parentObjectTypeId}``."""

    async def is_enabled_parent_type(
        self: "IsEnabledParentTypeMixin",
        parent_object_type_id: int,
        enabled_parent_type_ids: list[int],
        disabled_parent_type_ids: list[int],
        *,
        default_value: bool = False,
    ) -> bool:
        """Проверяет, разрешён ли тип объекта как родитель по спискам разрешённых/запрещённых.

        Отвечает на вопрос «может ли тип ``parent_object_type_id`` выступать родителем» с
        учётом двух явно переданных списков типов — белого (``enabled``) и чёрного
        (``disabled``). Учитывается иерархия типов: разрешение/запрет наследуется по дереву,
        поэтому проверка не сводится к простому вхождению id в список. Операция ЧТЕНИЯ
        метамодели: POST применяется лишь для передачи обоих списков телом запроса, ничего
        не изменяется.

        Когда применять: при валидации структуры состава/связей в UI или импортёре — нужно
        быстро понять, допустим ли конкретный тип-родитель в заданной политике применяемости
        (например, при фильтрации дерева доступных типов). Списки дочерних применяемостей по
        родителю — :meth:`applicability_child_object_type_ids` и родственные.

        Предусловие по id-пространству: все три аргумента — id ТИПОВ объектов
        (``ObjectTypeID``), не id объектов и не id версий.

        Args:
            parent_object_type_id: id проверяемого типа-РОДИТЕЛЯ (``ObjectTypeID``).
                Подставляется в путь.
            enabled_parent_type_ids: Белый список id типов, явно разрешённых как родители
                (``enabledParentTypeIds`` тела ``ImsApplicabilityParentTypeIdsDto``).
            disabled_parent_type_ids: Чёрный список id типов, явно запрещённых как родители
                (``disabledParentTypeIds`` того же DTO).
            default_value: Значение по умолчанию (query ``defaultValue``), возвращаемое
                сервером, когда тип не покрыт ни одним из списков. По умолчанию ``False``
                (fail-closed).

        Returns:
            ``True``, если тип разрешён как родитель в заданной политике, иначе ``False``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ok = await ips.is_enabled_parent_type(
                    1742, enabled_parent_type_ids=[1700], disabled_parent_type_ids=[]
                )
                if ok:
                    print("тип допустим как родитель")

        Notes:
            operationId ``Metadata_IsEnabledParentType``; путь
            ``POST /core/api/metadata/applicabilities/isEnabledParentType/``
            ``{parentObjectTypeId}`` с query ``defaultValue``. Тело —
            ``ImsApplicabilityParentTypeIdsDto`` (``{enabledParentTypeIds,
            disabledParentTypeIds}``), ответ — ``boolean``. ВНИМАНИЕ: вопреки исходному
            наброску сигнатуры, эндпоинт принимает не «id типа связи», а два списка
            родительских типов. См. объектной модели IPS.
        """
        body: dict[str, Any] = {
            "enabledParentTypeIds": enabled_parent_type_ids,
            "disabledParentTypeIds": disabled_parent_type_ids,
        }
        params: dict[str, Any] = {"defaultValue": str(default_value).lower()}
        path = f"/core/api/metadata/applicabilities/isEnabledParentType/{parent_object_type_id}"
        data = await self._request("post", path, json=body, params=params)
        return bool(data)
