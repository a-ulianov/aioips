"""Метод получения коллекции рангов подписи ЭЦП."""

from ...core import APIManager
from ...schemas.signs import IntKeyName


class SignRanksMixin(APIManager):
    """Реализует метод ``GET /api/signs/ranks`` (``Sign_GetSignRankCollection``)."""

    async def sign_ranks(self: "SignRanksMixin") -> list[IntKeyName]:
        """Возвращает коллекцию рангов подписи (уровней/категорий подписанта ЭЦП).

        Ранг подписи задаёт уровень или категорию электронной подписи (например,
        степень полномочий подписанта в маршруте). Метод отдаёт справочник доступных
        рангов в виде пар «числовой ключ + отображаемое имя»: ключ применяется при
        назначении ранга подписи, а имя служит для отображения в UI.

        Когда применять: чтобы получить перечень доступных рангов подписи (например,
        для выбора ранга при подписании или настройке графа). Это справочный read-метод
        без предусловий. Связанные справочники того же раздела — :meth:`sign_graphs`
        (графы подписания), :meth:`additional_sign_output_params` и
        :meth:`additional_user_output_params` (параметры вывода).

        Returns:
            Список элементов :class:`IntKeyName`; у каждого ``id`` — числовой ключ ранга
            (по умолчанию ``0``), ``display_name`` — отображаемое имя (может быть
            ``None``). Пустой список означает, что ранги подписи не определены.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ranks = await ips.sign_ranks()
                names = {r.id: r.display_name for r in ranks}

        Notes:
            operationId ``Sign_GetSignRankCollection``; путь ``GET /api/signs/ranks``
            (НЕ ``/core/api``). Ответ — голый массив
            ``Int64KeyAndNameCollectionItemOutContract``.
        """
        data = await self._request("get", "/api/signs/ranks")
        return [IntKeyName.model_validate(item) for item in data]
