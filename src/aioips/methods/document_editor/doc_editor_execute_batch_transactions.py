"""Метод выполнения пакета транзакций правок в редакторе документов (мутация)."""

from typing import Any

from ...core import APIManager


class DocEditorExecuteBatchTransactionsMixin(APIManager):
    """Реализует ``POST /core/api/documentEditor/execute/batch/transactions``.

    operationId ``DocumentEditor_ExecuteBatchOfTransactions``.
    """

    async def doc_editor_execute_batch_transactions(
        self: "DocEditorExecuteBatchTransactionsMixin",
        body: dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Выполняет пакет транзакций правок документа в редакторе (МУТАЦИЯ).

        Применяет к открытому документу набор транзакций изменений (создание/правка/
        удаление элементов, перестановка страниц и т.п.) одним запросом и возвращает
        сводку фактических изменений. Изменяет состояние документа на сервере, поэтому
        защищён ``confirm``. Результат правок можно затем зафиксировать через
        :meth:`doc_editor_save_document`.

        Защита: без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Тело запроса — пакет транзакций правок. Передаётся как есть. ``None`` —
                пустое тело ``{}``. Структура полиморфна (зависит от видов правок),
                поэтому принимается как ``dict[str, Any]``.
            confirm: Подтверждение мутации. Без ``True`` запрос не выполняется.

        Returns:
            Словарь ``ChangeResults`` «как есть» со значимыми ключами: ``changedPagesIds``
            (id изменённых страниц), ``createdElementIds`` (id созданных элементов),
            ``pageOrderChanged`` (изменился ли порядок страниц). Пустой словарь — сервер
            вернул пустой ответ.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.doc_editor_execute_batch_transactions(
                    {"transactions": [...]}, confirm=True,
                )
                print(result.get("changedPagesIds"))

        Notes:
            operationId ``DocumentEditor_ExecuteBatchOfTransactions``; путь
            ``POST /core/api/documentEditor/execute/batch/transactions`` (ответ —
            ``ChangeResults``). Beta-функциональность редактора документов.
        """
        if confirm is not True:
            raise ValueError(
                "doc_editor_execute_batch_transactions применяет правки на сервере; "
                "передайте confirm=True",
            )
        data: Any = await self._request(
            "post", "/core/api/documentEditor/execute/batch/transactions", json=body or {}
        )
        return data if isinstance(data, dict) else {}
