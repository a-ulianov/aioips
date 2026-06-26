"""Метод удаления временного файла из временного хранилища IPS."""

from urllib.parse import quote

from ...core import APIManager


class DeleteTempFileMixin(APIManager):
    """Реализует ``DELETE /core/api/files/temp/{tempFileName}`` (``Files_DeleteTempFile``)."""

    async def delete_temp_file(self: "DeleteTempFileMixin", temp_file_name: str) -> None:
        """Удаляет ранее загруженный временный файл из временного хранилища (МУТИРУЮЩАЯ).

        Завершает сценарий загрузки: удаляет временный файл, созданный
        :meth:`upload_temp_file`, если он не был прикреплён к объекту (или больше не
        нужен). Операция безопасна и обратима по смыслу — затрагивает только временное
        хранилище, а не объекты базы. Рекомендуется всегда удалять временные файлы,
        чтобы не оставлять мусор (например, в блоке ``finally``).

        Args:
            temp_file_name: Имя временного файла, возвращённое :meth:`upload_temp_file`.
                Кодируется в URL (допускаются спецсимволы и не-ASCII).

        Returns:
            ``None``. Успешное завершение означает, что временный файл удалён.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если файл не найден).

        Example:
            async with IPSClient(config=config) as ips:
                temp_name = await ips.upload_temp_file(b"data", "f.bin")
                await ips.delete_temp_file(temp_name)

        Notes:
            operationId ``Files_DeleteTempFile``; путь
            ``DELETE /core/api/files/temp/{tempFileName}``. Связанные:
            :meth:`upload_temp_file`.
        """
        encoded = quote(temp_file_name, safe="")
        await self._request("delete", f"/core/api/files/temp/{encoded}", json={})
