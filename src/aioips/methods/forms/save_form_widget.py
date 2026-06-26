"""Метод сохранения виджета формы IPS (мутация)."""

from typing import Any

from ...core import APIManager


class SaveFormWidgetMixin(APIManager):
    """Реализует ``POST /core/api/forms/saveFormWidget`` (``Forms_SaveFormWidget``)."""

    async def save_form_widget(
        self: "SaveFormWidgetMixin",
        widget: dict[str, Any],
        *,
        form_id: int | None = None,
        confirm: bool = False,
    ) -> None:
        """Сохраняет (создаёт/перезаписывает) виджет формы IPS (МУТАЦИЯ).

        Форма в IPS — это дерево виджетов (UI-элементов); см. :meth:`form` для чтения
        формы целиком. Метод записывает один виджет (``WidgetDto``) в указанную форму:
        если виджет с таким идентификатором уже существует — он перезаписывается, иначе
        добавляется. Это операция ЗАПИСИ, изменяющая оформление формы на сервере.

        Когда применять: при программном редактировании компоновки формы — добавлении
        нового UI-элемента или обновлении свойств существующего. Тело ``widget``
        соответствует DTO ``WidgetDto`` (рекурсивная UI-схема: виджет может содержать
        вложенные виджеты в поле ``widgets``).

        Обратимость: операция ОБРАТИМА по схеме write-same-back — прочитайте текущий
        виджет через :meth:`form`, сохраните его копию и для отката запишите обратно
        этим же методом. Рекомендуется сделать резервную копию исходного ``WidgetDto``
        перед изменением.

        Защита: меняет форму на сервере, поэтому защищена ``confirm`` — без ``confirm=True``
        поднимается :class:`ValueError` ещё ДО обращения к серверу.

        Args:
            widget: Тело виджета — словарь ``WidgetDto`` (ключи ``camelCase``, как их
                отдаёт :meth:`form`). Передаётся телом запроса (``json=widget``) без
                преобразований.
            form_id: Идентификатор формы (query-параметр ``formId``), в которую
                сохраняется виджет. ``None`` — параметр не передаётся (виджет адресуется
                полями самого тела).
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                form = await ips.form(540210)  # versionId формы
                root = form.model_dump(by_alias=True)
                await ips.save_form_widget(root, form_id=540, confirm=True)

        Notes:
            operationId ``Forms_SaveFormWidget``; путь
            ``POST /core/api/forms/saveFormWidget``. Query — ``formId`` (int64); тело —
            ``WidgetDto`` (``json=widget``). Ответ — void (None).
        """
        if confirm is not True:
            raise ValueError(
                "save_form_widget сохраняет виджет формы (меняет форму); передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if form_id is not None:
            params["formId"] = form_id
        await self._request("post", "/core/api/forms/saveFormWidget", params=params, json=widget)
        return None
