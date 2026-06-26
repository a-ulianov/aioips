"""Метод получения уникального имени файла от сервиса имён файлов IPS."""

from typing import Any

from ...core import APIManager


class FileUniqueNameMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getUniqueFileName``.

    operationId ``Files_GetUniqueFileName``.
    """

    async def file_unique_name(
        self: "FileUniqueNameMixin",
        *,
        file_name: str | None = None,
        id: int | None = None,
    ) -> str:
        """Возвращает уникальное имя файла на основе предложенного имени.

        Применяют, когда нужно гарантировать уникальность имени файла в
        пространстве имён сервиса имён файлов IPS перед его использованием
        (например, перед загрузкой/прикреплением). Сервер берёт ``file_name``
        как основу и, при необходимости, модифицирует его, чтобы избежать
        коллизии с уже занятыми именами.

        Это операция ЧТЕНИЯ (идемпотентная): существующие объекты и файлы не
        изменяются. Несмотря на метод POST, тело запроса не используется —
        параметры передаются в query; IPS, однако, требует наличия тела,
        поэтому отправляется пустой объект ``{}``.

        Args:
            file_name: Предлагаемое (исходное) имя файла (query ``fileName``).
                ``None`` — параметр не передаётся; сервер применит поведение по
                умолчанию.
            id: Идентификатор записи имени файла, который следует исключить из
                проверки на коллизию (query ``id``), — например, при
                переименовании уже существующей записи. ``None`` — параметр не
                передаётся (трактуется сервером как ``0``).

        Returns:
            Уникальное имя файла строкой. Пустая строка означает отсутствие
            имени в ответе сервера.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.file_unique_name(file_name="schema.pdf")
                # name == "schema.pdf" или, при коллизии, например "schema(1).pdf"

        Notes:
            operationId ``Files_GetUniqueFileName``. Часть сервиса имён файлов
            (``fileNamesService``). Связанные методы: :meth:`next_file_id`,
            :meth:`file_id_by_name`, :meth:`upload_temp_file`.
        """
        params: dict[str, Any] = {}
        if file_name is not None:
            params["fileName"] = "" if file_name is None else str(file_name)
        if id is not None:
            params["id"] = int(id) if id is not None else 0
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getUniqueFileName",
            json={},
            params=params or None,
        )
        return "" if data is None else str(data)
