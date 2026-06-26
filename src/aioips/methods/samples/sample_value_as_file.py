"""Метод получения значения sample-файла как файла (бинарное чтение)."""

from ...core import APIManager


class SampleValueAsFileMixin(APIManager):
    """Реализует ``GET /core/api/samples/values/{fileName}/asFile``.

    operationId ``Values_GetFile``.
    """

    async def sample_value_as_file(
        self: "SampleValueAsFileMixin",
        file_name: str,
    ) -> bytes:
        """Возвращает содержимое демо-файла как файл (учебный раздел, БАЙТЫ).

        Раздел ``samples`` — демонстрационный (учебный) API; на доменные объекты
        IPS не влияет. Метод отдаёт содержимое именованного файла как вложение
        (file-download). Применяйте как пример скачивания бинарных данных и для
        проверки бинарного транспорта клиента. Операция идемпотентна.

        Возврат — «сырые» ``bytes`` тела ответа (``application/octet-stream``), а
        НЕ JSON: ядро вызывается с ``raw_bytes=True``. Содержимое идентично
        :meth:`sample_value_as_content`; различие — семантика отдачи на сервере
        (как файл vs как контент).

        Args:
            file_name: Имя демо-файла (подставляется в путь как ``{fileName}``).

        Returns:
            Содержимое файла как ``bytes``. Пустой ответ сервера — ``b""``.

        Raises:
            IPSNotFoundError: Если файл с таким именем не найден.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                blob = await ips.sample_value_as_file("demo.bin")
                with open("demo.bin", "wb") as fh:
                    fh.write(blob)

        Notes:
            operationId ``Values_GetFile``; путь
            ``GET /core/api/samples/values/{fileName}/asFile``. Бинарный ответ
            (``raw_bytes=True``). Связанный метод:
            :meth:`sample_value_as_content`.
        """
        data = await self._request(
            "get",
            f"/core/api/samples/values/{file_name}/asFile",
            raw_bytes=True,
        )
        return data if isinstance(data, bytes) else b""
