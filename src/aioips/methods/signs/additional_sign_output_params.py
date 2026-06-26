"""Метод получения дополнительных параметров вывода подписи ЭЦП."""

from ...core import APIManager
from ...schemas.signs import IntKeyName


class AdditionalSignOutputParamsMixin(APIManager):
    """Реализует ``GET /api/signs/AdditionalSignOutputParams``.

    operationId ``Sign_GetAdditionalSignOutputParams``.
    """

    async def additional_sign_output_params(
        self: "AdditionalSignOutputParamsMixin",
    ) -> list[IntKeyName]:
        """Возвращает дополнительные параметры вывода подписи (штампа ЭЦП на документе).

        Дополнительные параметры вывода подписи управляют тем, какие сведения о подписи
        включать в её визуальное представление (штамп/отметку ЭЦП) при печати или
        отображении документа. Метод отдаёт справочник доступных параметров в виде пар
        «числовой ключ + отображаемое имя»: ключ применяется при настройке вывода
        подписи, а имя служит для отображения в UI.

        Когда применять: при настройке состава визуального штампа подписи на документе
        (какие поля показывать в отметке ЭЦП). Это справочный read-метод без предусловий.
        Парный справочник для отметки пользователя — :meth:`additional_user_output_params`;
        прочие справочники раздела — :meth:`sign_graphs`, :meth:`sign_ranks`.

        Returns:
            Список элементов :class:`IntKeyName`; у каждого ``id`` — числовой ключ
            параметра (по умолчанию ``0``), ``display_name`` — отображаемое имя (может
            быть ``None``). Пустой список означает отсутствие дополнительных параметров.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = await ips.additional_sign_output_params()
                print([p.display_name for p in params])

        Notes:
            operationId ``Sign_GetAdditionalSignOutputParams``; путь
            ``GET /api/signs/AdditionalSignOutputParams`` (НЕ ``/core/api``). Ответ —
            голый массив ``Int32KeyAndNameCollectionItemOutContract``.
        """
        data = await self._request("get", "/api/signs/AdditionalSignOutputParams")
        return [IntKeyName.model_validate(item) for item in data]
