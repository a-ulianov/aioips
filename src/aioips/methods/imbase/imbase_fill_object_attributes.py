"""Метод заполнения атрибутов объекта значениями из записи IMBASE (мутация)."""

from typing import Any

from ...core import APIManager


class ImBaseFillObjectAttributesMixin(APIManager):
    """Реализует ``POST /core/api/imbase/object/{destinationObjectId}/fillObjectAttributes``.

    operationId ``ImBase_FillImBaseObjectAttributes``.
    """

    async def imbase_fill_object_attributes(
        self: "ImBaseFillObjectAttributesMixin",
        destination_object_id: int,
        *,
        confirm: bool = False,
        object_type_id: int | None = None,
        base_id: int | None = None,
        record_id: int | None = None,
    ) -> None:
        """Заполняет атрибуты объекта значениями из записи IMBASE (МУТАЦИЯ; ``confirm``).

        Переносит значения из записи справочника IMBASE в атрибуты уже существующего
        объекта-приёмника ``destination_object_id``. Применяется, когда объект создан
        отдельно (или взят готовым), и его поля нужно заполнить данными справочной
        записи (например, подтянуть характеристики материала из базы материалов).
        Операция изменяет атрибуты объекта, поэтому по умолчанию НЕ выполняется:
        требуется явный ``confirm=True``, иначе поднимается :class:`ValueError` ещё до
        обращения к серверу.

        Предусловия: объект-приёмник должен быть в режиме, допускающем правку атрибутов
        (см. ``ObjectModifyModes``; обычно требуется checkout/новая версия) — иначе
        сервер вернёт ошибку. Связанный метод :meth:`imbase_create_object` создаёт
        объект из записи IMBASE «с нуля».

        Args:
            destination_object_id: Идентификатор ОБЪЕКТА-приёмника, чьи атрибуты
                заполняются; подставляется в путь URL.
            confirm: Подтверждение мутирующей операции. Без ``True`` метод не делает
                запрос (защитный гейт).
            object_type_id: Идентификатор типа объекта-приёмника (query
                ``objectTypeId``); ``None`` — параметр не передаётся.
            base_id: Идентификатор базы (каталога) IMBASE — источника значений (query
                ``baseId``); ``None`` — параметр не передаётся.
            record_id: Идентификатор записи IMBASE-таблицы — источника значений (query
                ``recordId``); ``None`` — параметр не передаётся.

        Returns:
            ``None`` — сервер отвечает без тела (HTTP 200, void). Успех = отсутствие
            исключения.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. если объект не в режиме
                правки).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.imbase_fill_object_attributes(
                    102550, object_type_id=3, base_id=204, record_id=1042, confirm=True
                )

        Notes:
            operationId ``ImBase_FillImBaseObjectAttributes``; путь
            ``POST /core/api/imbase/object/{destinationObjectId}/fillObjectAttributes``
            (тело отсутствует, ``{}``). Связанные: :meth:`imbase_create_object`,
            :meth:`object_check_out`, :meth:`object_check_in`. См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "Заполнение атрибутов изменяет объект: передайте confirm=True для подтверждения"
            )
        params: dict[str, Any] = {}
        if object_type_id is not None:
            params["objectTypeId"] = str(object_type_id)
        if base_id is not None:
            params["baseId"] = str(base_id)
        if record_id is not None:
            params["recordId"] = str(record_id)
        await self._request(
            "post",
            f"/core/api/imbase/object/{destination_object_id}/fillObjectAttributes",
            json={},
            params=params,
        )
