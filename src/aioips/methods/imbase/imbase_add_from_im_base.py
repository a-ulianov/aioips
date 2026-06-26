"""Метод добавления объекта из IMBASE в состав другого объекта (мутация)."""

from typing import Any

from ...core import APIManager


class ImBaseAddFromImBaseMixin(APIManager):
    """Реализует ``POST /core/api/imbase/object/composition`` (``ImBase_AddFromImBase``)."""

    async def imbase_add_from_im_base(
        self: "ImBaseAddFromImBaseMixin",
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Добавляет объект из справочника IMBASE в состав объекта (МУТАЦИЯ; ``confirm``).

        Создаёт (или переиспользует) объект из базы IMBASE и включает его в состав
        объекта-родителя, формируя связь состава. Применяется, когда запись справочника
        IMBASE должна войти в спецификацию/состав изделия (например, добавить
        стандартное изделие из базы крепежа в сборку). Операция изменяет состав,
        поэтому по умолчанию НЕ выполняется: требуется явный ``confirm=True``, иначе
        поднимается :class:`ValueError` ещё до обращения к серверу.

        Когда применять: чтобы добавить позицию из справочника IMBASE в состав
        существующего объекта. Отличие от :meth:`imbase_create_object` — здесь объект
        не просто создаётся, а сразу подвешивается в состав родителя (возвращается id
        связи). Откат — удаление созданного объекта (:meth:`object_delete`) или
        исключение из состава (:meth:`object_exclude_from_composition`).

        Args:
            request: Тело ``AddFromImBaseParamsDto`` как ``dict``. Ключи (camelCase):
                ``projObjectId`` (id ОБЪЕКТА-родителя, в чей состав добавляем),
                ``projObjectTypeId`` (id типа объекта-родителя), ``baseId`` (id базы
                IMBASE), ``recordId`` (id записи IMBASE-таблицы). Передаётся как есть.
            confirm: Подтверждение мутирующей операции. Без ``True`` метод не делает
                запрос (защитный гейт).

        Returns:
            Результат ``AddFromImBaseResultDto`` как ``dict[str, Any]``: ``objectId``
            (id созданного/добавленного ОБЪЕКТА) и ``relationId`` (id связи состава;
            нестабилен — не кэшировать). Пустой ``dict``, если сервер вернул не объект.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.imbase_add_from_im_base(
                    {
                        "projObjectId": 102550,
                        "projObjectTypeId": 3,
                        "baseId": 204,
                        "recordId": 1042,
                    },
                    confirm=True,
                )
                print(result["objectId"], result["relationId"])

        Notes:
            operationId ``ImBase_AddFromImBase``; путь
            ``POST /core/api/imbase/object/composition``; тело ``AddFromImBaseParamsDto``;
            ответ ``AddFromImBaseResultDto``. Связанные: :meth:`imbase_create_object`,
            :meth:`object_exclude_from_composition`, :meth:`object_delete`.
            См. [[ips-object-model]] (``projID``=ObjectID родителя; ``RelationID``
            нестабилен).
        """
        if confirm is not True:
            raise ValueError(
                "Добавление из IMBASE изменяет состав: передайте confirm=True для подтверждения"
            )
        data = await self._request("post", "/core/api/imbase/object/composition", json=request)
        return data if isinstance(data, dict) else {}
