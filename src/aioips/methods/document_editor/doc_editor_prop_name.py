"""Метод получения наименования назначаемого свойства редактора документов."""

from typing import Any

from ...core import APIManager


class DocEditorPropNameMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/getPropName`` (``DocumentEditor_GetPropEnum``)."""

    async def doc_editor_prop_name(
        self: "DocEditorPropNameMixin",
        *,
        props: int | None = None,
    ) -> str:
        """Возвращает наименование назначаемого свойства элемента редактора документов.

        Преобразует числовое значение перечисления свойств (``PropsValue``) в его
        читаемое наименование. Применяется как справочник для отображения свойств
        элементов документа в редакторе (beta-функциональность). Для свойств, которые
        нельзя назначать, используйте :meth:`doc_editor_non_assignable_prop_name`.

        Когда применять: чтобы получить человекочитаемое имя свойства по его коду
        (например, для построения интерфейса свойств или подписи). Метод только читает.

        Args:
            props: Числовой код свойства из перечисления ``PropsValue``. Если ``None``
                (по умолчанию), параметр в запрос не передаётся и сервер использует
                поведение по умолчанию.

        Returns:
            Наименование свойства строкой. Если сервер вернул пустой ответ (``None``),
            возвращается пустая строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.doc_editor_prop_name(props=1)

        Notes:
            operationId ``DocumentEditor_GetPropEnum``; путь
            ``GET /core/api/documentEditor/getPropName`` (query ``props``).
            Beta-функциональность редактора документов.
        """
        params: dict[str, Any] = {}
        if props is not None:
            params["props"] = props
        data = await self._request("get", "/core/api/documentEditor/getPropName", params=params)
        return str(data) if data is not None else ""
