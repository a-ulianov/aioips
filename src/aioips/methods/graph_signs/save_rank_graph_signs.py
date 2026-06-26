"""Метод записи настроек графических подписей (штампов ЭЦП) ранга (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.graph_signs import RankGraphSigns


class SaveRankGraphSignsMixin(APIManager):
    """Реализует ``POST /api/ranks/{rankId}/graphSigns``.

    operationId ``RankGraphSign_SaveRankGraphSigns``.
    """

    async def save_rank_graph_signs(
        self: "SaveRankGraphSignsMixin",
        rank_id: int,
        signs: list[RankGraphSigns] | list[dict[str, Any]],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки графических подписей ранга (МУТАЦИЯ, ``confirm``).

        Полностью переопределяет настройки графов подписания ранга — по записи на тип
        объекта: какие графы подписания и с какими правилами (простая/криптографическая
        подпись, запрет множественного подписания) применяются к объектам каждого типа в
        рамках ранга. Это **config-настройка подписей** (визуальные штампы / графы
        подписания), а НЕ права доступа. Парная запись к read-методу
        :meth:`rank_graph_signs`.

        Когда применять: чтобы задать/изменить настройки подписей ранга. Тело заменяет
        настройки целиком (перезапись, не слияние): передавайте полный итоговый список
        записей. Перечень типов объектов, которые можно добавить, отдаёт
        :meth:`rank_graph_sign_object_types`.

        Обратимость: операция обратима. Перед записью прочитайте текущие настройки парным
        :meth:`rank_graph_signs` и сохраните их; при откате запишите снимок обратно этим же
        методом (write-same-back). Тест: прочитать → записать тот же список обратно —
        состояние не меняется.

        Защита: мутация защищена ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            rank_id: Идентификатор ранга (``rankId``; id-пространство рангов подписания).
                Передаётся в пути.
            signs: Полный список настроек подписей ранга (:class:`RankGraphSigns`) или
                эквивалентных словарей (``RankGraphSignsContract``), по записи на тип
                объекта. Для точного round-trip передавайте «сырой» список из ответа
                :meth:`rank_graph_signs`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                current = await ips.rank_graph_signs(10)               # бэкап
                await ips.save_rank_graph_signs(10, current, confirm=True)  # запись обратно

        Notes:
            operationId ``RankGraphSign_SaveRankGraphSigns``; путь
            ``POST /api/ranks/{rankId}/graphSigns`` (НЕ ``/core/api``); тело — массив
            ``RankGraphSignsContract``. Парный read — :meth:`rank_graph_signs`.
        """
        if confirm is not True:
            raise ValueError(
                "save_rank_graph_signs мутирует настройки подписей; передайте confirm=True"
            )
        if signs and isinstance(signs[0], RankGraphSigns):
            payload: list[dict[str, Any]] = [
                s.model_dump(mode="json", by_alias=True, exclude_none=True)
                for s in signs
                if isinstance(s, RankGraphSigns)
            ]
        else:
            payload = [s for s in signs if isinstance(s, dict)]
        await self._request("post", f"/api/ranks/{rank_id}/graphSigns", json=payload)
        return None
