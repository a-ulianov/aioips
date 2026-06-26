"""Метод получения представления общих формул редактора документов."""

from typing import Any

from ...core import APIManager


class DocEditorGeneralFormulasViewMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/formulas/getGeneralFormulasView``.

    operationId ``DocumentEditor_GetGeneralFormulasView``.
    """

    async def doc_editor_general_formulas_view(
        self: "DocEditorGeneralFormulasViewMixin",
        formulas: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """Возвращает представление (вид) общих формул редактора документов.

        Принимает список описаний формул и отдаёт их визуальное представление
        (``GeneralFormulaView``): SVG-изображение, размеры, текст и поля формулы.
        Применяется для отрисовки формул при оформлении документа
        (beta-функциональность IPS).

        POST-verb, но операция ЧТЕНИЯ: вычисляет представление по переданным формулам и
        ничего не мутирует на сервере (идемпотентно).

        Args:
            formulas: Список описаний формул (``GeneralFormulaView``). Каждый элемент —
                словарь со значимыми ключами ``id``, ``itemComponentGuid``, ``fields``,
                ``formulaText`` и др. Передаётся как есть. ``None`` — пустой список
                ``[]``. Структура зависит от формулы, поэтому принимается как
                ``list[dict[str, Any]]``.

        Returns:
            Список словарей ``GeneralFormulaView`` «как есть»; у каждого среди значимых
            полей ``svgImage`` (изображение), ``height`` / ``width`` (размеры),
            ``formulaText``. Пустой список — формул нет либо сервер вернул пустой ответ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                views = await ips.doc_editor_general_formulas_view(
                    [{"id": 1, "formulaText": "a+b"}],
                )
                for v in views:
                    print(v.get("svgImage"))

        Notes:
            operationId ``DocumentEditor_GetGeneralFormulasView``; путь
            ``POST /core/api/documentEditor/formulas/getGeneralFormulasView`` (тело и
            ответ — массив ``GeneralFormulaView``). Beta-функциональность редактора.
        """
        data: Any = await self._request(
            "post",
            "/core/api/documentEditor/formulas/getGeneralFormulasView",
            json=formulas or [],
        )
        return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []
