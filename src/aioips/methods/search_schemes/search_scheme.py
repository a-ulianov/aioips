"""Метод получения поисковой схемы (выборки) по идентификатору объекта."""

from ...core import APIManager
from ...schemas.search_schemes import SearchScheme


class SearchSchemeMixin(APIManager):
    """Реализует ``GET /core/api/searchSchemes/{objectId}/getById`` (``SearchSchemes_GetById``)."""

    async def search_scheme(self: "SearchSchemeMixin", object_id: int) -> SearchScheme:
        """Возвращает сохранённую поисковую схему (выборку) по идентификатору её объекта.

        Поисковая схема — это именованная конфигурация поиска объектов: направление
        обхода связей, правило версий, типы искомых объектов, набор выводимых колонок
        и привязка к ролям. Метод загружает такую схему целиком, чтобы её можно было
        выполнить, разобрать или отредактировать.

        Когда применять: когда нужно прочитать параметры готовой выборки (например,
        перед запуском поиска по ней или для отображения её настроек). Чтобы узнать,
        по каким атрибутам выборка строит условия фильтрации, используйте
        :meth:`condition_structure_info`.

        Предусловие по id-пространству: аргумент — идентификатор ОБЪЕКТА поисковой
        схемы (``objectID`` / F_OBJECT_ID), а не идентификатор её версии.

        Args:
            object_id: Идентификатор объекта поисковой схемы (``objectID`` /
                F_OBJECT_ID), под которым схема сохранена в IPS.

        Returns:
            Поисковая схема по схеме :class:`SearchScheme`. Значимые поля:
            ``search_schema_name`` — имя выборки, ``searched_object_types`` — типы
            искомых объектов, ``columns`` — дополнительные колонки результата,
            ``version_rule`` — правило отбора версий.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если схема не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                scheme = await ips.search_scheme(102550)  # 102550 = objectID схемы
                print(scheme.search_schema_name, scheme.searched_object_types)

        Notes:
            operationId ``SearchSchemes_GetById``; путь
            ``GET /core/api/searchSchemes/{objectId}/getById`` (тело — ``SearchSchemaDto``).
        """
        data = await self._request("get", f"/core/api/searchSchemes/{object_id}/getById")
        return SearchScheme.model_validate(data)
