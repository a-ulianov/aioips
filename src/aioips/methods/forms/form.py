"""Метод получения формы (виджета) по идентификатору версии."""

from ...core import APIManager
from ...schemas.forms import Widget


class FormMixin(APIManager):
    """Реализует ``GET /core/api/forms/{versionId}`` (``Forms_GetForm``)."""

    async def form(
        self: "FormMixin",
        version_id: int,
    ) -> Widget | None:
        """Возвращает форму (корневой виджет) по идентификатору версии.

        Форма в IPS — это дерево виджетов; корневой виджет (сама форма) содержит
        вложенные виджеты в поле ``widgets``. Ответ сервера обёрнут в
        ``WidgetDtoNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо :class:`Widget`, либо ``None``.

        Предусловие по id-пространству (критично): аргумент — идентификатор ВЕРСИИ
        формы (``versionId`` / F_ID), а НЕ идентификатор объекта (``objectID``).

        Когда применять: чтобы загрузить описание формы по её версии (например, для
        рендеринга или анализа состава виджетов). Список форм, применимых к версии,
        даёт :meth:`forms_for`.

        Args:
            version_id: Идентификатор ВЕРСИИ формы (``versionId`` / F_ID). Не
                идентификатор объекта.

        Returns:
            Форма по схеме :class:`Widget` либо ``None``, если форма с такой версией не
            найдена (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                form = await ips.form(102551)
                if form is not None:
                    print(form.name, len(form.widgets))

        Notes:
            operationId ``Forms_GetForm``; путь ``GET /core/api/forms/{versionId}``;
            ответ — ``WidgetDtoNullableResultDto`` (разворачивается в ``Widget``/``None``).
            Внимание: путь без завершающего слеша; ``/{versionId}/formsFor`` — другой
            эндпоинт (см. :meth:`forms_for`).
        """
        data = await self._request("get", f"/core/api/forms/{version_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return Widget.model_validate(entity) if entity is not None else None
