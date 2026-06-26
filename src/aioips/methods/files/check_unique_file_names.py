"""Метод проверки имён файлов на уникальность в контексте записи (IPS)."""

from typing import Any

from ...core import APIManager


class CheckUniqueFileNamesMixin(APIManager):
    """Реализует ``POST /core/api/files/{id}/checkUniqueFileNames``.

    operationId ``Files_CheckFileNamesForUnique``.
    """

    async def check_unique_file_names(
        self: "CheckUniqueFileNamesMixin",
        file_id: int,
        file_names: list[str],
    ) -> list[dict[str, Any]]:
        """Проверяет список имён файлов на уникальность относительно записи файла.

        Применяют перед загрузкой/прикреплением, чтобы выяснить, какие из
        предложенных имён уже заняты, и получить рекомендованную (свободную)
        замену. В отличие от :meth:`file_unique_name` (одно имя → одно
        уникальное), здесь проверяется сразу набор имён в контексте записи
        ``file_id``.

        Это операция ЧТЕНИЯ. Несмотря на метод POST, существующие файлы не
        изменяются. Тело запроса — голый JSON-массив строк (проверяемые имена).

        Предусловие по id-пространству: ``file_id`` (path ``id``) — идентификатор
        записи файла (пространство сервиса имён файлов), исключаемой из проверки
        на коллизию (например, при переименовании самой этой записи), а НЕ
        ``objectID`` объекта.

        Args:
            file_id: Идентификатор записи файла (path ``id``, int64),
                исключаемый из проверки на коллизию.
            file_names: Список проверяемых имён файлов (тело — массив строк).

        Returns:
            Список результатов проверки (в swagger — массив
            ``FileNameUniqueCheckResultDto``), отдаваемый как список словарей.
            Значимые ключи каждого элемента: ``originalFileName`` (исходное имя),
            ``recommendedFileName`` (рекомендованное свободное имя),
            ``isOriginalFileNameUnique`` (флаг уникальности исходного имени).
            Пустой список — если сервер вернул не-список.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                results = await ips.check_unique_file_names(
                    778899, ["schema.pdf", "draft.pdf"]
                )
                taken = [
                    r["originalFileName"]
                    for r in results
                    if not r.get("isOriginalFileNameUnique")
                ]

        Notes:
            operationId ``Files_CheckFileNamesForUnique``. Связанные методы:
            :meth:`file_unique_name`, :meth:`get_file_names_table`.
        """
        data = await self._request(
            "post",
            f"/core/api/files/{file_id}/checkUniqueFileNames",
            json=list(file_names),
        )
        return data if isinstance(data, list) else []
