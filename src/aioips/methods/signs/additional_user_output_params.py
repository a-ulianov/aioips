"""Метод получения дополнительных параметров вывода пользователя ЭЦП."""

from ...core import APIManager
from ...schemas.signs import IntKeyName


class AdditionalUserOutputParamsMixin(APIManager):
    """Реализует ``GET /api/signs/AdditionalUserOutputParams``.

    operationId ``Sign_GetAdditionalUserOutputParams``.
    """

    async def additional_user_output_params(
        self: "AdditionalUserOutputParamsMixin",
    ) -> list[IntKeyName]:
        """Возвращает дополнительные параметры вывода сведений о пользователе (подписанте).

        Дополнительные параметры вывода пользователя управляют тем, какие сведения о
        подписанте (например, должность, подразделение) включать в визуальное
        представление подписи — отметку/штамп ЭЦП — при печати или отображении документа.
        Метод отдаёт справочник доступных параметров в виде пар «числовой ключ +
        отображаемое имя»: ключ применяется при настройке вывода, а имя — для UI.

        Когда применять: при настройке состава сведений о подписанте в штампе ЭЦП. Это
        справочный read-метод без предусловий. Парный справочник для самой подписи —
        :meth:`additional_sign_output_params`; прочие справочники раздела —
        :meth:`sign_graphs`, :meth:`sign_ranks`.

        Returns:
            Список элементов :class:`IntKeyName`; у каждого ``id`` — числовой ключ
            параметра (по умолчанию ``0``), ``display_name`` — отображаемое имя (может
            быть ``None``). Пустой список означает отсутствие дополнительных параметров.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = await ips.additional_user_output_params()
                print([p.id for p in params])

        Notes:
            operationId ``Sign_GetAdditionalUserOutputParams``; путь
            ``GET /api/signs/AdditionalUserOutputParams`` (НЕ ``/core/api``). Ответ —
            голый массив ``Int32KeyAndNameCollectionItemOutContract``.
        """
        data = await self._request("get", "/api/signs/AdditionalUserOutputParams")
        return [IntKeyName.model_validate(item) for item in data]
