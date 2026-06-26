"""Метод получения применимости типа атрибута по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import AttributeTypeApplicability


class AttributeTypeApplicabilityMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributeTypeApplicability/{id}``."""

    async def attribute_type_applicability(
        self: "AttributeTypeApplicabilityMixin",
        attribute_type_id: int,
    ) -> AttributeTypeApplicability:
        """Возвращает категорию применимости типа атрибута по его идентификатору.

        Применимость сообщает, к каким сущностям объектной модели задействован тип
        атрибута: к объектам (``objectType``), к связям (``relationType``) или ни к чему
        (``none``). В swagger ответ — голый строковый enum ``IMSAttributeTypeApplicability``,
        возвращаемый НАПРЯМУЮ (без обёртки ``...NullableResultDto``); строка валидируется
        в :class:`AttributeTypeApplicability`, значение доступно через ``.root``.

        Когда применять: чтобы понять контекст использования типа атрибута перед
        операциями над объектами/связями. Булев предикат «используется ли вообще» —
        :meth:`attribute_is_in_use`; аналог по GUID — :meth:`attribute_type_applicability_by_guid`.

        Args:
            attribute_type_id: Идентификатор ТИПА атрибута (id-пространство типов
                атрибутов метаданных, не значение атрибута объекта).

        Returns:
            Применимость по схеме :class:`AttributeTypeApplicability`; конкретное значение
            (``none`` / ``objectType`` / ``relationType``) — в атрибуте ``root``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                applicability = await ips.attribute_type_applicability(1029)
                print(applicability.root)

        Notes:
            operationId ``Metadata_GetAttributeTypeApplicabilityById``; путь
            ``GET /core/api/metadata/attributeTypeApplicability/{id}`` (ответ — голый
            строковый enum). Связанные методы: :meth:`attribute_is_in_use`,
            :meth:`attribute_type_applicability_by_guid`.
        """
        path = f"/core/api/metadata/attributeTypeApplicability/{attribute_type_id}"
        data = await self._request("get", path)
        return AttributeTypeApplicability.model_validate(data)
