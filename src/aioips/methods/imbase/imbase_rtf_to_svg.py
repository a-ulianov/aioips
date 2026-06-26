"""Конвертер значения-RTF атрибута IMBASE в base64-SVG."""

from ...core import APIManager


class ImBaseRtfToSvgMixin(APIManager):
    """Реализует ``POST .../object/converter/rtfToSvg/{width}``.

    operationId ``ImBase_ConvertRtfToBase64Svg``.
    """

    async def imbase_rtf_to_svg(
        self: "ImBaseRtfToSvgMixin",
        rtf: str,
        width: int,
    ) -> str:
        r"""Конвертирует RTF-значение атрибута IMBASE в SVG (base64-строка).

        Рендерит форматированное RTF-значение атрибута справочника IMBASE в
        векторное изображение SVG и возвращает его закодированным в base64 —
        удобно для встраивания в веб-интерфейс (``data:image/svg+xml;base64,…``).
        Это чистая функция-преобразование: операция не привязана к объекту и
        ничего не меняет на сервере.

        Когда применять: чтобы показать RTF-значение с сохранением форматирования
        как картинку фиксированной ширины. Несмотря на метод POST, побочных
        эффектов нет. Тело запроса — сама RTF-строка, сериализованная как
        JSON-строка; ширина передаётся в пути.

        Args:
            rtf: Исходное значение в формате RTF (строка). Передаётся в теле как
                JSON-строка.
            width: Ширина результирующего SVG в пикселях (path-параметр ``width``,
                int). Высота подбирается по содержимому.

        Returns:
            SVG-изображение, закодированное в base64 (``str``). Пустая строка —
            если входной RTF пуст.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                svg_b64 = await ips.imbase_rtf_to_svg(r"{\rtf1 H\sub 2 O}", 240)
                src = f"data:image/svg+xml;base64,{svg_b64}"

        Notes:
            operationId ``ImBase_ConvertRtfToBase64Svg``; путь
            ``POST /core/api/imbase/object/converter/rtfToSvg/{width}`` (тело —
            JSON-строка, ответ — строка base64). Парный конвертер в текст —
            :meth:`imbase_rtf_to_plain_text`.
        """
        data = await self._request(
            "post",
            f"/core/api/imbase/object/converter/rtfToSvg/{width}",
            json=rtf,
        )
        return data if isinstance(data, str) else str(data)
