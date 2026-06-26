"""Метод форменного поиска коллекции объектов (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.find_collection_options import FindCollectionOptions
from ...schemas.forms.form_object import FormObjectDto


class FindCollectionMixin(APIManager):
    """Реализует ``POST /core/api/forms/findCollection``.

    operationId ``Forms_FindCollection``.
    """

    async def find_collection(
        self: "FindCollectionMixin",
        options: FindCollectionOptions,
    ) -> list[FormObjectDto]:
        """Подбирает коллекцию объектов по параметрам формы (чтение через POST).

        Возвращает коллекцию объектов, соответствующих контексту формы (тип/версия
        объекта, контекст выбора, фильтры, пагинация). Несмотря на HTTP-метод POST, это
        операция ЧТЕНИЯ: сервер ничего не изменяет, тело служит контейнером параметров.

        Когда применять: основной форменный поиск — когда нужно получить набор объектов
        формы постранично. Родственные методы: :meth:`find_applicability`
        (применимость), :meth:`find_composition` (состав).

        Предусловие по id-пространствам (см. :class:`FindCollectionOptions`): поля
        ``*_version_id`` — версии (F_ID), ``object_type_id`` — тип объекта.

        Args:
            options: Параметры поиска (:class:`FindCollectionOptions`): контекст формы,
                колонки результата, фильтры и пагинация.

        Returns:
            Список объектов по схеме :class:`FormObjectDto`. Пустой список — ничего не
            найдено под заданные параметры.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                opts = FindCollectionOptions(object_type_id=1742, page=0, page_size=50)
                objects = await ips.find_collection(opts)
                print([o.caption for o in objects])

        Notes:
            operationId ``Forms_FindCollection``; путь
            ``POST /core/api/forms/findCollection``; тело — ``FindCollectionOptions``;
            ответ — массив ``FormObjectDto``. См. объектной модели IPS.
        """
        payload = options.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/forms/findCollection", json=payload)
        items = data if isinstance(data, list) else []
        return [FormObjectDto.model_validate(item) for item in items]
