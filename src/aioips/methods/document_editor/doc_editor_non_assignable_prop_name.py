"""Метод получения наименования неназначаемого свойства редактора документов."""

from typing import Any

from ...core import APIManager


class DocEditorNonAssignablePropNameMixin(APIManager):
    """Реализует ``GET /core/api/documentEditor/getNonAssignablePropName``.

    operationId ``DocumentEditor_GetNonAssignablePropEnum``.
    """

    async def doc_editor_non_assignable_prop_name(
        self: "DocEditorNonAssignablePropNameMixin",
        *,
        props: int | None = None,
    ) -> str:
        """Возвращает наименование неназначаемого свойства элемента редактора документов.

        Преобразует числовое значение перечисления неназначаемых свойств
        (``NonAssignableProps``) в его читаемое наименование. Неназначаемые свойства —
        это атрибуты элементов документа, которые отображаются, но не редактируются
        пользователем. Для назначаемых свойств используйте :meth:`doc_editor_prop_name`.

        Когда применять: чтобы получить человекочитаемое имя неназначаемого свойства по
        его коду (например, для интерфейса свойств элемента). Метод только читает.

        Args:
            props: Числовой код свойства из перечисления ``NonAssignableProps``. Если
                ``None`` (по умолчанию), параметр в запрос не передаётся и сервер
                использует поведение по умолчанию.

        Returns:
            Наименование свойства строкой. Если сервер вернул пустой ответ (``None``),
            возвращается пустая строка ``""``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.doc_editor_non_assignable_prop_name(props=2)

        Notes:
            operationId ``DocumentEditor_GetNonAssignablePropEnum``; путь
            ``GET /core/api/documentEditor/getNonAssignablePropName`` (query ``props``).
            Beta-функциональность редактора документов.
        """
        params: dict[str, Any] = {}
        if props is not None:
            params["props"] = props
        data = await self._request(
            "get", "/core/api/documentEditor/getNonAssignablePropName", params=params
        )
        return str(data) if data is not None else ""
