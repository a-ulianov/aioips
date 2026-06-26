"""Метод проверки возможности перевода объекта на следующий шаг ЖЦ."""

from typing import Any

from ...core import APIManager


class ObjectCanSetNextLcStepMixin(APIManager):
    """Реализует ``.../{objectId}/сanSetNextLCStep`` (``Objects_CanSetNextLCStep``)."""

    async def object_can_set_next_lc_step(
        self: "ObjectCanSetNextLcStepMixin",
        object_id: int,
        *,
        next_step_id: int | None = None,
    ) -> dict[str, Any]:
        """Проверяет, можно ли перевести объект на следующий шаг ЖЦ (ПРОВЕРКА, без мутации).

        Возвращает пару «можно ли перейти» + «причина запрета»: серверный ответ
        ``BooleanStringTuple`` с полями ``item1`` (``bool`` — допустим ли переход) и
        ``item2`` (``str | None`` — текст причины, если переход запрещён). В отличие от
        :meth:`object_validate_set_next_lc_step` (которая выполняет проверочные действия и
        при запрете поднимает ошибку), этот метод лишь сообщает результат проверки, не
        бросая исключение при недопустимости перехода.

        Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА
        (``F_OBJECT_ID``).

        Notes:
            ⚠️ Баг IPS API: в URL первый символ сегмента — КИРИЛЛИЧЕСКАЯ ``с`` (U+0441),
            а не латинская ``c``: ``.../сanSetNextLCStep``. Путь в коде намеренно содержит
            кириллическую букву; не «исправляйте» её на латинскую — иначе сервер вернёт 404.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``F_OBJECT_ID``), проверяемого перед переходом.
            next_step_id: Идентификатор целевого шага ЖЦ (query ``nextStepId``); ``None`` —
                параметр не передаётся (серверный дефолт — следующий шаг по схеме).

        Returns:
            Словарь ``{"item1": bool, "item2": str | None}``: ``item1`` — допустим ли
            переход, ``item2`` — причина запрета (или ``None``/пусто, если переход допустим).
            Пустой словарь, если сервер не вернул результат.

        Raises:
            IPSError: При ошибочном ответе сервера (сам факт недопустимости перехода
                исключением НЕ является — см. поле ``item1``).

        Example:
            async with IPSClient(config=config) as ips:
                check = await ips.object_can_set_next_lc_step(102550, next_step_id=42)
                if not check["item1"]:
                    print("Переход запрещён:", check["item2"])

        References:
            ``Objects_CanSetNextLCStep``. Связанные: :meth:`object_validate_set_next_lc_step`.
        """
        params: dict[str, Any] = {}
        if next_step_id is not None:
            params["nextStepId"] = str(next_step_id)
        data = await self._request(
            "post",
            f"/core/api/objects/{object_id}/сanSetNextLCStep",
            json={},
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return result if isinstance(result, dict) else {}
