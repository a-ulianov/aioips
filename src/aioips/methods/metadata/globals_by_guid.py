"""Метод определения вида сущности метаданных по GUID."""

from uuid import UUID

from ...core import APIManager


class GlobalsByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/globals/byGuid/{guid}``."""

    async def globals_by_guid(
        self: "GlobalsByGuidMixin",
        guid: UUID | str,
    ) -> str:
        """Определяет ВИД сущности метаданных по её GUID.

        GUID в метаданных IPS уникален в пределах всей базы, но сам по себе не говорит,
        ЧТО за сущность за ним стоит. Метод классифицирует GUID, возвращая строковое
        значение перечисления ``IMSGlobals``: тип объекта, тип атрибута, группа атрибутов,
        уровень/схема/шаг ЖЦ, тип связи либо ``unknown`` (GUID неизвестен метаданным).

        Когда применять: как «диспетчер» — получив произвольный GUID метаданных, сначала
        выяснить его вид, чтобы затем вызвать профильный метод (например, при
        ``imsObjectType`` — :meth:`object_type_by_guid`, при ``imsAttributeType`` —
        :meth:`attribute_type_by_guid`). Человекочитаемую подпись по тому же GUID даёт
        :meth:`displayable_by_guid`.

        Args:
            guid: GUID сущности метаданных. Подставляется в URL как есть (``UUID`` или
                строка). Id-пространство ТИПОВ/метаданных, не ``objectGUID`` конкретного
                объекта.

        Returns:
            Строковое значение перечисления ``IMSGlobals`` — одно из: ``"unknown"``,
            ``"imsAttributeType"``, ``"imsAttributeGroup"``, ``"imsLifeCycleLevel"``,
            ``"imsLifeCycleScheme"``, ``"imsLifeCycleStep"``, ``"imsObjectType"``,
            ``"imsRelationType"``. ``"unknown"`` — GUID не принадлежит ни одной известной
            сущности метаданных.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                kind = await ips.globals_by_guid("cad001c5-306c-11d8-b4e9-00304f19f545")
                if kind == "imsObjectType":
                    obj_type = await ips.object_type_by_guid(
                        "cad001c5-306c-11d8-b4e9-00304f19f545"
                    )

        Notes:
            operationId ``Metadata_GetGlobalsByGuid``; путь
            ``GET /core/api/metadata/globals/byGuid/{guid}``. Ответ — голое строковое
            значение enum ``IMSGlobals`` (НЕ объект и НЕ обёртка ``...NullableResultDto``):
            «отсутствие» сущности кодируется значением ``"unknown"``, поэтому возвращается
            ``str``, а не ``None``. Связанный метод — :meth:`displayable_by_guid`.
        """
        data = await self._request("get", f"/core/api/metadata/globals/byGuid/{guid}")
        return str(data)
