"""Метод получения суффиксов документов IPS (чтение через POST)."""

from typing import Any

from ...core import APIManager


class DocSuffixesMixin(APIManager):
    """Реализует ``POST /core/api/docs/GetDocSuffixes``.

    operationId ``Documents_GetDocSuffixes``.
    """

    async def doc_suffixes(self: "DocSuffixesMixin") -> list[Any]:
        """Возвращает список суффиксов документов, известных серверу (чтение).

        Суффикс документа — строковая метка, дополняющая обозначение документа
        (например, для различения исполнений/вариантов одного и того же
        документа). Метод отдаёт полный перечень суффиксов, настроенных в
        системе. Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ — сервер
        ничего не изменяет, тело запроса пустое (``{}``).

        Когда применять: чтобы получить справочник допустимых суффиксов
        (например, для выпадающего списка при оформлении документа).
        Предусловий нет.

        Returns:
            Список суффиксов в исходном виде ответа сервера. По swagger это
            массив строк (``list[str]``); элементы передаются как есть, без
            преобразования. Пустой список ``[]``, если суффиксов нет или сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                suffixes = await ips.doc_suffixes()

        Notes:
            operationId ``Documents_GetDocSuffixes``; путь
            ``POST /core/api/docs/GetDocSuffixes``. Тело не передаётся (``{}``
            против 415). По swagger ответ — массив строк. См. [[ips-object-model]].
        """
        data = await self._request("post", "/core/api/docs/GetDocSuffixes", json={})
        return list(data) if isinstance(data, list) else []
