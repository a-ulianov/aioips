"""Метод получения коллекции графов подписания ЭЦП."""

from ...core import APIManager
from ...schemas.signs import StringKeyName


class SignGraphsMixin(APIManager):
    """Реализует метод ``GET /api/signs/graphs`` (``Sign_GetSignGraphCollection``)."""

    async def sign_graphs(self: "SignGraphsMixin") -> list[StringKeyName]:
        """Возвращает коллекцию графов подписания (схем согласования/подписания ЭЦП).

        Граф подписания — это именованная схема маршрута электронной подписи,
        определяющая, кто и в каком порядке подписывает документ. Метод отдаёт
        справочник доступных графов в виде пар «строковый ключ + отображаемое имя»:
        ключ применяется при назначении графа на документ/операцию подписания, а имя
        служит для отображения в UI выбора графа.

        Когда применять: чтобы получить список доступных графов подписания (например,
        для выпадающего списка при настройке маршрута ЭЦП). Это справочный read-метод
        без предусловий. Числовые справочники того же раздела — :meth:`sign_ranks`,
        :meth:`additional_sign_output_params`, :meth:`additional_user_output_params`.

        Returns:
            Список элементов :class:`StringKeyName`; у каждого ``id`` — строковый ключ
            графа, ``display_name`` — его отображаемое имя. Пустой список означает, что
            графы подписания не определены. Любое поле элемента может быть ``None``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                graphs = await ips.sign_graphs()
                for g in graphs:
                    print(g.id, g.display_name)

        Notes:
            operationId ``Sign_GetSignGraphCollection``; путь ``GET /api/signs/graphs``
            (НЕ ``/core/api``). Ответ — голый массив
            ``StringKeyAndNameCollectionItemOutContract``.
        """
        data = await self._request("get", "/api/signs/graphs")
        return [StringKeyName.model_validate(item) for item in data]
