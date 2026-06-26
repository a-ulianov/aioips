"""Метод получения демо-приветствия (samples/values)."""

from typing import Any

from ...core import APIManager


class SampleValuesMixin(APIManager):
    """Реализует ``GET /core/api/samples/values`` (``Values_GetGreeting``)."""

    async def sample_values(self: "SampleValuesMixin") -> dict[str, Any]:
        """Возвращает демо-приветствие для текущего пользователя (учебный раздел).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты IPS
        не влияет. Метод применяют как простую проверку авторизации и доступности
        сервера: успешный ответ означает, что токен принят и сервис отвечает.
        Предусловий нет; операция идемпотентна.

        Returns:
            Приветствие (``UserGreetingDTO``) как ``dict[str, Any]`` с ключом ``text``
            (непустая строка). Для типизированного разбора см.
            :class:`aioips.schemas.samples.UserGreeting`.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                greeting = await ips.sample_values()
                print(greeting["text"])

        Notes:
            operationId ``Values_GetGreeting``; путь ``GET /core/api/samples/values``
            (объект ``UserGreetingDTO``). Бинарные эндпоинты ``/values/{fileName}/asFile``
            и т.п. в этом разделе не реализованы.
        """
        data = await self._request("get", "/core/api/samples/values")
        return dict(data)
