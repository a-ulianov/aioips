"""Метод форменного поиска применимости объектов (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.find_collection_options import FindCollectionOptions
from ...schemas.forms.form_object import FormObjectDto


class FindApplicabilityMixin(APIManager):
    """Реализует ``POST /core/api/forms/findApplicability``.

    operationId ``Forms_FindApplicability``.
    """

    async def find_applicability(
        self: "FindApplicabilityMixin",
        options: FindCollectionOptions,
    ) -> list[FormObjectDto]:
        """Подбирает объекты по применимости в контексте формы (чтение через POST).

        Возвращает объекты, применимые к заданному контексту формы (тип/версия объекта,
        контекст выбора, фильтры по типам атрибутов/связей). Несмотря на HTTP-метод POST,
        это операция ЧТЕНИЯ: сервер ничего не изменяет, тело используется лишь как
        контейнер параметров поиска (их слишком много для query-строки).

        Когда применять: когда нужно показать перечень объектов, «подходящих» форме в
        текущем контексте применимости. Родственные поиски: :meth:`find_collection`
        (общая коллекция), :meth:`find_composition` (состав).

        Предусловие по id-пространствам (см. :class:`FindCollectionOptions`): поля
        ``*_version_id`` — версии (F_ID), ``object_type_id`` — тип объекта.

        Args:
            options: Параметры поиска (:class:`FindCollectionOptions`): контекст формы,
                колонки результата, фильтры и пагинация.

        Returns:
            Список объектов по схеме :class:`FormObjectDto`. Пустой список — ничего не
            подобрано под заданные параметры.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                opts = FindCollectionOptions(object_type_id=1742, object_version_id=102551)
                objects = await ips.find_applicability(opts)
                print([o.caption for o in objects])

        Notes:
            operationId ``Forms_FindApplicability``; путь
            ``POST /core/api/forms/findApplicability``; тело — ``FindCollectionOptions``;
            ответ — массив ``FormObjectDto``. См. [[ips-object-model]].
        """
        payload = options.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/forms/findApplicability", json=payload)
        items = data if isinstance(data, list) else []
        return [FormObjectDto.model_validate(item) for item in items]
