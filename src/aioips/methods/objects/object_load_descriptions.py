"""Метод пакетной загрузки описаний версий объектов."""

from typing import Any

from ...core import APIManager


class ObjectLoadDescriptionsMixin(APIManager):
    """Реализует ``Objects_LoadDescriptions`` (загрузка описаний версий объектов)."""

    async def object_load_descriptions(
        self: "ObjectLoadDescriptionsMixin",
        version_ids: list[int],
        *,
        throw_exception: bool = False,
    ) -> list[Any]:
        """Загружает краткие описания версий объектов по списку их идентификаторов.

        Метод сервиса ``IObjectsCheckOutServerService``: возвращает облегчённые
        описания (caption / тип / идентификаторы / режим) для каждой запрошенной
        ВЕРСИИ. Это операция **только чтения** — она НЕ извлекает объекты на
        редактирование (в отличие от :meth:`object_check_out_versions`). Применяйте,
        когда перед пакетным checkout нужно заранее узнать характеристики версий
        (тип, заголовок, текущий режим извлечения) без побочных эффектов.

        Предусловие по id-пространству (важно): тело — список идентификаторов ВЕРСИЙ
        (``id`` / F_ID), а НЕ идентификаторов объектов (``objectID`` / F_OBJECT_ID).

        Args:
            version_ids: Список идентификаторов ВЕРСИЙ объектов (``id`` / F_ID),
                для которых нужно загрузить описания. Сериализуется как голый
                JSON-массив ``list[int]`` в теле запроса.
            throw_exception: Если ``True``, сервер бросит исключение при ошибке по
                любой из версий; если ``False`` (по умолчанию) — проблемные элементы
                просто не попадут в результат (query ``throwException``).

        Returns:
            Список «сырых» описаний версий (элементы ``ObjectCheckOutVersionsItem``)
            как ``list[Any]``: каждый словарь содержит ключи ``caption``,
            ``objectTypeID``, ``objectID``, ``id``, ``mode``. Пустой список, если
            ничего не загружено.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                descrs = await ips.object_load_descriptions([102550, 102551])
                for d in descrs:
                    print(d["caption"], d["mode"])

        Notes:
            ``operationId``: ``Objects_LoadDescriptions``. Эндпоинт
            ``POST /core/api/objects/ObjectsCheckOutServerService/LoadDescriptions``.
            Тело — голый массив ``list[int]``; ответ — голый массив (не result-обёртка).
            Связанные методы: :meth:`object_check_out_versions`,
            :meth:`object_rollback_check_out`. См. объектной модели IPS.
        """
        params: dict[str, Any] = {"throwException": str(throw_exception).lower()}
        data = await self._request(
            "post",
            "/core/api/objects/ObjectsCheckOutServerService/LoadDescriptions",
            json=version_ids,
            params=params,
        )
        return data if isinstance(data, list) else []
