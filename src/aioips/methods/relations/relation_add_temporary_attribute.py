"""Метод добавления временного атрибута связи (запись)."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class RelationAddTemporaryAttributeMixin(APIManager):
    """Реализует ``RelationAttributes_AddTemporaryAttribute`` (временный атрибут связи)."""

    async def relation_add_temporary_attribute(
        self: "RelationAddTemporaryAttributeMixin",
        relation_id: int,
        attribute_id: int,
        *,
        fail_if_exists: bool = False,
        values: list[Any] | None = None,
    ) -> Attribute:
        """Добавляет к СВЯЗИ временный атрибут заданного типа и инициализирует значения.

        Временный атрибут существует у связи лишь в текущем сеансе работы с ней и не
        входит в постоянную модель типа атрибутов: применяйте, когда связи нужно
        присвоить характеристику, которой у её типа штатно нет (служебные/вычисляемые
        пометки на время редактирования). Связь — атрибутируемая сущность
        (``IDBAttributable``). Для записи постоянных атрибутов используйте
        :meth:`relation_set_attributes` / :meth:`relation_set_attribute_values`.

        ПРЕДУСЛОВИЕ (запись связи): объект-РОДИТЕЛЬ связи (``projID`` = ObjectID
        родителя) должен быть извлечён на редактирование (checkout) в режиме,
        разрешающем правку на текущем шаге ЖЦ. Без активного checkout родителя
        добавление невозможно. Это отличает запись от чтения атрибутов связи.

        Отличие от временного атрибута ОБЪЕКТА: там адресация по ``objectID`` и атрибут
        добавляется самому объекту; здесь по ``relationID`` — атрибут принадлежит связи,
        а не её объектам-концам.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).
            attribute_id: Идентификатор ТИПА атрибута, который добавить связи.
            fail_if_exists: Если ``True`` и атрибут уже есть — сервер вернёт ошибку;
                если ``False`` (по умолчанию) — существующий атрибут используется как есть.
            values: Начальные значения атрибута (типы зависят от ``FieldTypes``).
                ``None`` — без инициализации значений (передаётся пустой список).

        Returns:
            Добавленный атрибут связи по схеме :class:`Attribute` (тело ответа —
            ``AttributeDto``). Содержит ``attribute_id`` и заданные ``values``.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родитель связи не
                извлечён на редактирование, либо ``fail_if_exists=True`` и атрибут
                уже существует).

        Example:
            async with IPSClient(config=config) as ips:
                # Предполагается, что родитель связи уже на checkout.
                attr = await ips.relation_add_temporary_attribute(
                    700123, attribute_id=205, values=["A1"]
                )

        Notes:
            ``operationId``: ``RelationAttributes_AddTemporaryAttribute``. Тело запроса —
            ``TempAttributeDto`` (ключи ``attributeId``, ``failIfExists``, ``values``);
            ответ — одиночный ``AttributeDto``. См. [[ips-object-model]] (разделы
            «Атрибуты», «Связи и состав»).
        """
        payload: dict[str, Any] = {
            "attributeId": attribute_id,
            "failIfExists": fail_if_exists,
            "values": values or [],
        }
        data = await self._request(
            "post",
            f"/core/api/relations/{relation_id}/attributes/tempAttribute",
            json=payload,
        )
        return Attribute.model_validate(data)
