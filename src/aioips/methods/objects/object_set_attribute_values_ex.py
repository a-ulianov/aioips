"""Метод расширенной записи значений атрибутов объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import SetAttributeValuesExBody


class ObjectSetAttributeValuesExMixin(APIManager):
    """Реализует ``ObjectAttributes_SetAttributeValuesEx`` (расширенная запись атрибутов)."""

    async def object_set_attribute_values_ex(
        self: "ObjectSetAttributeValuesExMixin",
        object_id: int,
        body: SetAttributeValuesExBody,
        *,
        log_history: bool = True,
    ) -> dict[str, Any]:
        """Записывает значения атрибутов в расширенном режиме (с режимами извлечения).

        Расширенный вариант :meth:`object_set_attribute_values`: помимо значений и флагов
        поведения, тело несёт набор режимов извлечения ``modes`` (``GetAttributeValuesModes``),
        управляющих формой данных, и возвращает словарь сведений об ошибках по элементам
        (а не список записанных значений). Применяйте, когда нужно точечно управлять
        составом ответа или получить пер-атрибутные ошибки записи.

        ПРЕДУСЛОВИЕ (жизненный цикл): запись возможна, только если объект извлечён на
        редактирование (checkout). Метод НЕ делает checkout сам (см. :meth:`object_check_out`).

        Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
        (``objectID`` / F_OBJECT_ID), общий для версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID).
            body: Параметры расширенной записи (:class:`SetAttributeValuesExBody`):
                значения атрибутов, флаги поведения и режимы извлечения. Сериализуется
                в тело запроса.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            Словарь ``{ключ: сведения_об_исключении}`` (``StringExceptionInfoDtoDictionary``):
            по записанным/проблемным атрибутам. Пустой словарь, если ошибок нет или сервер
            ничего не вернул.

        Raises:
            IPSConflictError: Если объект не извлечён на редактирование (конфликт ЖЦ).
            IPSForbiddenError: При отсутствии прав на запись атрибутов.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects import AttributeValues, SetAttributeValuesExBody

            async with IPSClient(config=config) as ips:
                # Объект 102550 предварительно извлечён на редактирование (checkout).
                errors = await ips.object_set_attribute_values_ex(
                    102550,
                    SetAttributeValuesExBody(
                        attribute_values=[AttributeValues(attribute_id=12, values=["550.07.305"])]
                    ),
                )

        References:
            ``ObjectAttributes_SetAttributeValuesEx``. Связанные:
            :meth:`object_set_attribute_values`, :meth:`object_check_out`.
        """
        payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/attributeValuesEx",
            json=payload,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return result if isinstance(result, dict) else {}
