"""Метод выборки демо-сообщений по фильтру (samples)."""

from typing import Any

from ...core import APIManager


class MessagesByFilterMixin(APIManager):
    """Реализует ``GET /core/api/samples/messages/queries/byFilter``.

    operationId ``Messages_GetAllByFilter``.
    """

    async def messages_by_filter(
        self: "MessagesByFilterMixin",
        contains_text: str,
        *,
        from_time: str | None = None,
        to_time: str | None = None,
    ) -> list[dict[str, Any]]:
        """Возвращает демо-сообщения, отфильтрованные по подстроке текста и интервалу дат.

        Раздел ``samples`` — демонстрационный (учебный) API сообщений; на доменные
        объекты IPS не влияет. Применяйте для отбора сообщений по вхождению подстроки и
        (опционально) по окну времени изменения. Для полного списка без фильтра —
        :meth:`messages`.

        Args:
            contains_text: Обязательная подстрока, которую должен содержать текст
                сообщения (query ``containsText``).
            from_time: Нижняя граница времени (включительно) в формате ISO-8601
                ``date-time`` (query ``fromTime``). ``None`` — граница не задаётся.
            to_time: Верхняя граница времени в формате ISO-8601 ``date-time``
                (query ``toTime``). ``None`` — граница не задаётся.

        Returns:
            Список подходящих сообщений (``FullMessageDTO``) как
            ``list[dict[str, Any]]``. Пустой список — совпадений нет. Для
            типизированного разбора см. :class:`aioips.schemas.samples.FullMessage`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                found = await ips.messages_by_filter(
                    "привет", from_time="2026-01-01T00:00:00Z"
                )

        Notes:
            operationId ``Messages_GetAllByFilter``; путь
            ``GET /core/api/samples/messages/queries/byFilter`` (массив
            ``FullMessageDTO``). Связанный метод: :meth:`messages`.
        """
        params: dict[str, Any] = {"containsText": contains_text}
        if from_time is not None:
            params["fromTime"] = from_time
        if to_time is not None:
            params["toTime"] = to_time
        data = await self._request(
            "get",
            "/core/api/samples/messages/queries/byFilter",
            params=params,
        )
        return list(data) if data is not None else []
