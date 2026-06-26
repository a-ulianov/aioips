"""Метод форменного поиска списка объектов по версиям (чтение через POST)."""

from ...core import APIManager
from ...schemas.forms.form_object import FormObjectDto
from ...schemas.forms.version_id_and_columns_request import VersionIdAndColumns4Request


class FindObjectsListMixin(APIManager):
    """Реализует ``POST /core/api/forms/findObjectsList``.

    operationId ``Forms_FindObjectsList``.
    """

    async def find_objects_list(
        self: "FindObjectsListMixin",
        request: VersionIdAndColumns4Request,
    ) -> list[FormObjectDto]:
        """Возвращает строки списка объектов формы по версиям (чтение через POST).

        Отдаёт объекты для заданного перечня версий с указанными колонками результата.
        Несмотря на HTTP-метод POST, это операция ЧТЕНИЯ: сервер ничего не изменяет, тело
        служит контейнером параметров (список версий, колонки, режим трактовки id).

        Когда применять: когда уже известен список версий объектов и нужно получить их
        строки/значения колонок в раскладке формы (например, для дозагрузки таблицы).
        В отличие от :meth:`find_collection`, выборка идёт по явному списку версий,
        а не по фильтрам.

        Предусловие по id-пространству (см. :class:`VersionIdAndColumns4Request`):
        ``object_version_ids`` — идентификаторы ВЕРСИЙ (F_ID), не объектов.

        Args:
            request: Параметры запроса (:class:`VersionIdAndColumns4Request`): версии
                объектов, колонки результата, флаг трактовки идентификаторов.

        Returns:
            Список объектов по схеме :class:`FormObjectDto`. Пустой список — для
            переданных версий ничего не найдено.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                req = VersionIdAndColumns4Request(object_version_ids=[102550, 102551])
                objects = await ips.find_objects_list(req)
                print([o.caption for o in objects])

        Notes:
            operationId ``Forms_FindObjectsList``; путь
            ``POST /core/api/forms/findObjectsList``; тело —
            ``VersionIdAndColumns4Request``; ответ — массив ``FormObjectDto``.
            См. [[ips-object-model]].
        """
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/forms/findObjectsList", json=payload)
        items = data if isinstance(data, list) else []
        return [FormObjectDto.model_validate(item) for item in items]
