"""Метод валидации перевода объекта на следующий шаг ЖЦ."""

from typing import Any

from ...core import APIManager


class ObjectValidateSetNextLcStepMixin(APIManager):
    """Реализует ``.../{objectId}/validateSetNextLCStep`` (``Objects_ValidateSetNextLCStep``)."""

    async def object_validate_set_next_lc_step(
        self: "ObjectValidateSetNextLcStepMixin",
        object_id: int,
        *,
        next_step_id: int | None = None,
    ) -> None:
        """Проверяет допустимость перевода объекта на следующий шаг ЖЦ (МУТИРУЮЩАЯ операция).

        Выполняет серверную проверку готовности объекта к переходу на указанный шаг
        жизненного цикла (предшествует фактической смене шага). Метод может выполнять
        проверочные действия и менять серверное состояние, поэтому помечен как мутирующий.
        При непрохождении проверок сервер возвращает ошибку.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``F_OBJECT_ID``), проверяемого перед переходом.
            next_step_id: Идентификатор целевого шага ЖЦ (query ``nextStepId``); ``None`` —
                параметр не передаётся (серверный дефолт — следующий шаг по схеме).

        Returns:
            ``None`` — метод ничего не возвращает (тип ответа ``void``); успешный вызов
            означает, что перевод допустим.

        Raises:
            IPSConflictError: Если перевод на следующий шаг ЖЦ недопустим (не выполнены
                условия перехода).
            IPSError: При иной ошибке сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.object_validate_set_next_lc_step(102550, next_step_id=42)

        References:
            ``Objects_ValidateSetNextLCStep``.
        """
        params: dict[str, Any] = {}
        if next_step_id is not None:
            params["nextStepId"] = str(next_step_id)
        await self._request(
            "post",
            f"/core/api/objects/{object_id}/validateSetNextLCStep",
            json={},
            params=params,
        )
        return None
