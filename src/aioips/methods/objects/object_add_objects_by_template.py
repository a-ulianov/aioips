"""Метод добавления объектов в состав по шаблону-таблице."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AddObjectsByTemplateBody


class ObjectAddObjectsByTemplateMixin(APIManager):
    """Реализует ``.../{objectId}/addObjectsByTemplate`` (``Objects_AddObjectsByTemplate``)."""

    async def object_add_objects_by_template(
        self: "ObjectAddObjectsByTemplateMixin",
        object_id: int,
        body: AddObjectsByTemplateBody,
        *,
        log_history: bool = True,
    ) -> None:
        """Добавляет объекты в состав объекта по шаблону-таблице (МУТИРУЮЩАЯ операция).

        По шаблону-таблице (``body.template_id``) в состав объекта добавляются строки-объекты;
        ``body.object_ids`` задаёт двумерный набор id (по строкам шаблона), либо ``None`` —
        добавляются все строки шаблона. Это альтернатива поэлементному
        :meth:`object_include_in_composition`, когда состав формируется по заранее
        определённому шаблону.

        Предусловие: объект-владелец состава обычно должен быть в режиме редактирования
        (см. :meth:`object_check_out` / :meth:`object_edit`), иначе сервер отклонит
        изменение состава.

        Args:
            object_id: Идентификатор объекта (``objectId``), в состав которого добавляются
                объекты по шаблону.
            body: Параметры добавления (:class:`AddObjectsByTemplateBody`): обязательный
                ``template_id``, необязательные ``object_ids`` и ``context_rule``.
                Сериализуется в тело запроса.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            ``None`` — метод ничего не возвращает (тип ответа ``Nothing``); успешный вызов
            означает, что объекты добавлены в состав.

        Raises:
            IPSConflictError: Если объект не в режиме редактирования либо нарушены правила
                применяемости/состава.
            IPSError: При иной ошибке сервера.

        Example:
            from aioips.schemas.objects import AddObjectsByTemplateBody

            async with IPSClient(config=config) as ips:
                await ips.object_add_objects_by_template(
                    102551,
                    AddObjectsByTemplateBody(template_id=701, object_ids=[[33001], [33002]]),
                )

        References:
            ``Objects_AddObjectsByTemplate``. Связанные: :meth:`object_include_in_composition`,
            :meth:`object_composition_with_params`.
        """
        payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        await self._request(
            "post",
            f"/core/api/objects/{object_id}/addObjectsByTemplate",
            json=payload,
            params=params,
        )
        return None
