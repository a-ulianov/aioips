"""Метод получения значения sample-файла как контента (бинарное чтение)."""

from ...core import APIManager


class SampleValueAsContentMixin(APIManager):
    """Реализует ``GET /core/api/samples/values/{fileName}/asContent``.

    operationId ``Values_GetFileContent``.
    """

    async def sample_value_as_content(
        self: "SampleValueAsContentMixin",
        file_name: str,
    ) -> bytes:
        """Возвращает содержимое демо-файла как контент (учебный раздел, БАЙТЫ).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты
        IPS не влияет. Метод отдаёт содержимое именованного файла «как контент»
        (inline, без заголовка вложения). Применяйте как пример встраивания
        бинарных данных и для проверки бинарного транспорта клиента. Операция
        идемпотентна.

        Возврат — «сырые» ``bytes`` тела ответа (``application/octet-stream``), а
        НЕ JSON: ядро вызывается с ``raw_bytes=True``. Содержимое идентично
        :meth:`sample_value_as_file`; различие — семантика отдачи на сервере
        (как контент vs как файл).

        Args:
            file_name: Имя демо-файла (подставляется в путь как ``{fileName}``).

        Returns:
            Содержимое файла как ``bytes``. Пустой ответ сервера — ``b""``.

        Raises:
            IPSNotFoundError: Если файл с таким именем не найден.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                blob = await ips.sample_value_as_content("demo.bin")
                print(len(blob))

        Notes:
            operationId ``Values_GetFileContent``; путь
            ``GET /core/api/samples/values/{fileName}/asContent``. Бинарный ответ
            (``raw_bytes=True``). Связанный метод: :meth:`sample_value_as_file`.
        """
        data = await self._request(
            "get",
            f"/core/api/samples/values/{file_name}/asContent",
            raw_bytes=True,
        )
        return data if isinstance(data, bytes) else b""
