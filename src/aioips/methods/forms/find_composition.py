"""Метод форменного поиска состава объектов (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.find_collection_options import FindCollectionOptions
from ...schemas.forms.form_object import FormObjectDto


class FindCompositionMixin(APIManager):
    """Реализует ``POST /core/api/forms/findComposition``.

    operationId ``Forms_FindComposition``.
    """

    async def find_composition(
        self: "FindCompositionMixin",
        options: FindCollectionOptions,
    ) -> list[FormObjectDto]:
        """Подбирает объекты состава формы по параметрам (чтение через POST).

        Возвращает объекты, входящие в состав (композицию) формы согласно заданному
        контексту (тип/версия объекта, фильтры, пагинация). Несмотря на HTTP-метод POST,
        это операция ЧТЕНИЯ: сервер ничего не изменяет, тело служит контейнером
        параметров поиска.

        Когда применять: когда нужен именно состав формы (вложенные/дочерние объекты), а
        не общая коллекция. Родственные методы: :meth:`find_collection` (коллекция),
        :meth:`find_applicability` (применимость).

        Предусловие по id-пространствам (см. :class:`FindCollectionOptions`): поля
        ``*_version_id`` — версии (F_ID), ``object_type_id`` — тип объекта.

        Args:
            options: Параметры поиска (:class:`FindCollectionOptions`): контекст формы,
                колонки результата, фильтры и пагинация.

        Returns:
            Список объектов состава по схеме :class:`FormObjectDto`. Пустой список —
            состав пуст либо ничего не найдено под параметры.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                opts = FindCollectionOptions(object_version_id=102551)
                objects = await ips.find_composition(opts)
                print([o.caption for o in objects])

        Notes:
            operationId ``Forms_FindComposition``; путь
            ``POST /core/api/forms/findComposition``; тело — ``FindCollectionOptions``;
            ответ — массив ``FormObjectDto``. См. [[ips-object-model]].
        """
        payload = options.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/forms/findComposition", json=payload)
        items = data if isinstance(data, list) else []
        return [FormObjectDto.model_validate(item) for item in items]
