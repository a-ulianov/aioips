"""Метод расширенной записи значений атрибутов связи."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import SetAttributeValuesExBody


class RelationSetAttributeValuesExMixin(APIManager):
    """Реализует ``RelationAttributes_SetAttributeValuesEx`` (расширенная запись атрибутов)."""

    async def relation_set_attribute_values_ex(
        self: "RelationSetAttributeValuesExMixin",
        relation_id: int,
        body: SetAttributeValuesExBody,
        *,
        log_history: bool = True,
    ) -> dict[str, Any]:
        """Записывает значения атрибутов СВЯЗИ в расширенном режиме (с режимами извлечения).

        Расширенный вариант :meth:`relation_set_attribute_values`: помимо значений и
        флагов поведения, тело несёт набор режимов извлечения ``modes``
        (``GetAttributeValuesModes``), управляющих формой данных, а ответ — словарь
        пер-атрибутных сведений об ошибках (а не список записанных значений).
        Применяйте, когда нужно тонко управлять составом ответа или получить ошибки
        записи по конкретным атрибутам связи.

        ПРЕДУСЛОВИЕ (запись связи): объект-РОДИТЕЛЬ связи (``projID`` = ObjectID
        родителя) должен быть извлечён на редактирование (checkout) в режиме,
        разрешающем правку на текущем шаге ЖЦ. Без активного checkout родителя запись
        невозможна. Метод НЕ делает checkout сам.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).
            body: Параметры расширенной записи (:class:`SetAttributeValuesExBody`):
                значения атрибутов, флаги поведения и режимы извлечения. Сериализуется
                через ``model_dump(mode="json", by_alias=True, exclude_none=True)`` в
                тело ``SetAttributeValuesDto``.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            Словарь ``{ключ: сведения_об_исключении}``
            (``StringExceptionInfoDtoDictionary``) — поле ``result`` ответа: по
            записанным/проблемным атрибутам. Пустой словарь, если ошибок нет либо
            сервер ничего не вернул.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родитель связи не
                извлечён на редактирование или правка запрещена шагом ЖЦ).

        Example:
            from aioips.schemas.objects import AttributeValues, SetAttributeValuesExBody

            async with IPSClient(config=config) as ips:
                # Родитель связи 700123 уже на checkout.
                errors = await ips.relation_set_attribute_values_ex(
                    700123,
                    SetAttributeValuesExBody(
                        attribute_values=[AttributeValues(attribute_id=205, values=["A1"])]
                    ),
                )

        Notes:
            ``operationId``: ``RelationAttributes_SetAttributeValuesEx``. Эндпоинт
            ``POST /core/api/relations/{relationId}/attributeValuesEx``. Тело —
            ``SetAttributeValuesDto``; ответ —
            ``StringExceptionInfoDtoDictionaryProcessResultWithLogInfoDto`` (поле
            ``result``). Связанные методы: :meth:`relation_set_attribute_values`,
            :meth:`object_set_attribute_values_ex`.
        """
        payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/relations/{relation_id}/attributeValuesEx",
            json=payload,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return result if isinstance(result, dict) else {}
