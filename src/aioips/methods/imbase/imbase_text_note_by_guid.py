"""Метод получения текстовой заметки объекта IMBASE по GUID."""

from urllib.parse import quote

from ...core import APIManager


class ImBaseTextNoteByGuidMixin(APIManager):
    """Реализует ``GET /core/api/imbase/object/textNote/byGuid/{guid}``."""

    async def imbase_text_note_by_guid(
        self: "ImBaseTextNoteByGuidMixin",
        guid: str,
    ) -> str:
        """Возвращает значение атрибута-текстовой заметки объекта IMBASE по GUID.

        Атрибут «текстовая заметка» (``ftTextNote``) хранит длинный текст, привязанный
        к объекту IMBASE. Метод отдаёт его содержимое как строку. Ответ сервера — сама
        строка (не объект-обёртка).

        Когда применять: чтобы прочитать текстовую заметку записи IMBASE, когда известен
        её GUID. GUID кодируется в URL. Объект IMBASE адресуется здесь по GUID, а не по
        числовому id.

        Args:
            guid: Глобальный идентификатор объекта IMBASE (GUID); кодируется в URL.

        Returns:
            Текст заметки (``str``). Пустая строка означает, что заметка пуста.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если объект с таким
                GUID не найден).

        Example:
            async with IPSClient(config=config) as ips:
                note = await ips.imbase_text_note_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(note)

        Notes:
            operationId ``ImBase_GetTextNoteAttributeByGuid``; путь
            ``GET /core/api/imbase/object/textNote/byGuid/{guid}``.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/imbase/object/textNote/byGuid/{encoded_guid}"
        data = await self._request("get", path)
        return str(data)
