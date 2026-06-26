"""Конвертер значения-RTF атрибута IMBASE в простой текст."""

from ...core import APIManager


class ImBaseRtfToPlainTextMixin(APIManager):
    """Реализует ``POST .../object/converter/rtfToPlainText``.

    operationId ``ImBase_GetPlainTextFromRtf``.
    """

    async def imbase_rtf_to_plain_text(
        self: "ImBaseRtfToPlainTextMixin",
        rtf: str,
    ) -> str:
        r"""Конвертирует RTF-значение атрибута IMBASE в простой текст.

        Значения некоторых атрибутов справочника IMBASE хранятся в формате RTF
        (форматированный текст). Этот конвертер снимает разметку и возвращает
        «плоский» текст — пригодный для поиска, индексации или показа там, где
        форматирование не нужно. Это чистая функция-преобразование: операция не
        обращается к конкретному объекту и ничего не изменяет на сервере.

        Когда применять: чтобы получить текстовое представление RTF-значения
        атрибута. Несмотря на метод POST, побочных эффектов нет. Тело запроса —
        сама RTF-строка, сериализованная как JSON-строка (content-type
        ``application/json``), а не как объект.

        Args:
            rtf: Исходное значение в формате RTF (строка). Передаётся в теле как
                JSON-строка.

        Returns:
            Простой текст без RTF-разметки (``str``). Пустая строка — если входной
            RTF пуст или не содержит текста.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                text = await ips.imbase_rtf_to_plain_text(
                    r"{\rtf1 Ребро жёсткости}"
                )
                print(text)  # Ребро жёсткости

        Notes:
            operationId ``ImBase_GetPlainTextFromRtf``; путь
            ``POST /core/api/imbase/object/converter/rtfToPlainText``
            (тело — JSON-строка, ответ — строка). Парный конвертер в SVG —
            :meth:`imbase_rtf_to_svg`.
        """
        data = await self._request(
            "post",
            "/core/api/imbase/object/converter/rtfToPlainText",
            json=rtf,
        )
        return data if isinstance(data, str) else str(data)
