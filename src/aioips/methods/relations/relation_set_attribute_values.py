"""Метод установки значений атрибутов связи (запись)."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AttributeValues


class RelationSetAttributeValuesMixin(APIManager):
    """Реализует ``RelationAttributes_SetAttributeValues`` (запись значений атрибутов связи)."""

    async def relation_set_attribute_values(
        self: "RelationSetAttributeValuesMixin",
        relation_id: int,
        attribute_values: list[AttributeValues],
        *,
        delete_not_existing: bool = False,
        dont_delete_blobs: bool = False,
        return_delta: bool = False,
        log_history: bool = True,
        modes: list[str] | None = None,
    ) -> list[AttributeValues]:
        """Записывает значения атрибутов СВЯЗИ списком ``AttributeValues``.

        Точечная запись значений собственных атрибутов связи: каждый элемент
        :class:`AttributeValues` описывает атрибут и его значения (с типом, режимами,
        описаниями). Применяйте, когда нужно задать/обновить значения по их спискам
        (в т.ч. множественные), опционально удалив атрибуты, не вошедшие в передачу.
        Связь — атрибутируемая сущность (``IDBAttributable``) со своими характеристиками.
        Если нужно записать готовые DTO ``Attribute`` целиком — см.
        :meth:`relation_set_attributes`.

        ПРЕДУСЛОВИЕ (запись связи): объект-РОДИТЕЛЬ связи (``projID`` = ObjectID
        родителя) должен быть извлечён на редактирование (checkout) в режиме,
        разрешающем правку на текущем шаге ЖЦ. Без активного checkout родителя запись
        невозможна. Чтение (:meth:`relation_attributes_values`) checkout не требует.

        Отличие от записи значений атрибутов ОБЪЕКТА: запись объекта адресуется по
        ``objectID`` и меняет сам объект; здесь адресация — по ``relationID``, меняются
        собственные атрибуты связи, а не её объекты-концы.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. объектной модели IPS).
            attribute_values: Значения атрибутов к записи (схема :class:`AttributeValues`).
                Каждый сериализуется через
                ``model_dump(mode="json", by_alias=True, exclude_none=True)`` в массив
                ``attributeValues`` тела ``SetAttributeValuesDto``. Если у элемента
                ``read_only=True`` — он игнорируется сервером.
            delete_not_existing: Если ``True``, атрибуты, отсутствующие в переданном
                списке, будут удалены (используйте с осторожностью). По умолчанию ``False``.
            dont_delete_blobs: Если ``True``, blob-значения не удаляются с диска при
                удалении атрибутов. Имеет смысл вместе с ``delete_not_existing``.
                По умолчанию ``False``.
            return_delta: Если ``True``, сервер вернёт только реально изменённые атрибуты;
                если ``False`` (по умолчанию) — ``result`` будет ``null`` (вернётся
                пустой список).
            log_history: Если ``True`` (по умолчанию), сервер логирует историю
                модификаций; если ``False`` — без журналирования.
            modes: Набор флагов формирования результата (enum-строки
                ``GetAttributeValuesModes``: includeName/includeGuid/includeBlobs и т.п.).
                ``None`` — серверный режим по умолчанию.

        Returns:
            Список изменённых атрибутов (схема :class:`AttributeValues`) — поле ``result``
            ответа ``AttributeValuesDtoListProcessResultWithLogInfoDto``. Пустой список,
            если ``return_delta=False`` либо сервер вернул ``result=null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родитель связи не
                извлечён на редактирование или правка запрещена шагом ЖЦ).

        Example:
            from aioips.schemas.objects import AttributeValues

            async with IPSClient(config=config) as ips:
                # Предполагается, что родитель связи уже на checkout.
                changed = await ips.relation_set_attribute_values(
                    700123,
                    [AttributeValues(attributeId=205, values=["A1"])],
                    return_delta=True,
                )

        Notes:
            ``operationId``: ``RelationAttributes_SetAttributeValues``. Тело запроса —
            ``SetAttributeValuesDto`` (ключи ``attributeValues``,
            ``deleteNotExistingAttribute``, ``dontDeleteBlobs``, ``returnDelta``,
            ``modes``); ответ — обёртка с журналом модификаций. См. объектной модели IPS
            (разделы «Редактирование», «Связи и состав») и граблям.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        payload: dict[str, Any] = {
            "attributeValues": [
                v.model_dump(mode="json", by_alias=True, exclude_none=True)
                for v in attribute_values
            ],
            "deleteNotExistingAttribute": delete_not_existing,
            "dontDeleteBlobs": dont_delete_blobs,
            "returnDelta": return_delta,
            "modes": modes or [],
        }
        data = await self._request(
            "post",
            f"/core/api/relations/{relation_id}/attributeValues",
            json=payload,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        items = result if isinstance(result, list) else []
        return [AttributeValues.model_validate(item) for item in items]
