"""Метод round-trip числового значения (samples)."""

from ...core import APIManager


class SampleValueAsLongMixin(APIManager):
    """Реализует ``GET /core/api/samples/values/{value}/asLong``.

    operationId ``Values_RoundtripLong``.
    """

    async def sample_value_as_long(self: "SampleValueAsLongMixin", value: int) -> int:
        """Возвращает переданное число (round-trip ``long``) учебного раздела.

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты
        IPS не влияет. Метод принимает целое в пути и возвращает его же (round-trip
        проверка сериализации ``long``). Применяйте как пример числового
        контракта и для проверки разбора числового JSON-ответа клиента. Операция
        идемпотентна.

        Args:
            value: Целое число (подставляется в путь как ``{value}``).
                Возвращается сервером без изменений.

        Returns:
            То же число как ``int``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                n = await ips.sample_value_as_long(42)
                assert n == 42

        Notes:
            operationId ``Values_RoundtripLong``; путь
            ``GET /core/api/samples/values/{value}/asLong`` (ответ — целое JSON).
        """
        data = await self._request(
            "get",
            f"/core/api/samples/values/{value}/asLong",
        )
        return int(data)
