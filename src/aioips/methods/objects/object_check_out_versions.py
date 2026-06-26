"""Метод пакетного извлечения версий объектов на редактирование (check-out)."""

from typing import Any

from ...core import APIManager


class ObjectCheckOutVersionsMixin(APIManager):
    """Реализует ``Objects_CheckOutVersions`` (пакетный check-out версий)."""

    async def object_check_out_versions(
        self: "ObjectCheckOutVersionsMixin",
        version_ids: list[int],
        *,
        throw_exception: bool = False,
    ) -> dict[str, Any]:
        """Извлекает несколько версий объектов на редактирование одним запросом.

        Пакетный аналог :meth:`object_check_out` для группы версий: метод сервиса
        ``IObjectsCheckOutServerService`` ставит каждую запрошенную ВЕРСИЮ в режим
        редактирования и возвращает структуру результата, которую затем можно
        целиком передать в :meth:`object_rollback_check_out` для отката всей операции.
        Применяйте, когда нужно атомарно подготовить набор версий к правке, сохранив
        «токен» для обратимого отката.

        ⚠️ Это МУТИРУЮЩАЯ операция (создаёт рабочие копии), но **обратимая**: откат
        выполняется :meth:`object_rollback_check_out` с тем же возвращённым словарём.

        Предусловие по id-пространству (важно): тело — список идентификаторов ВЕРСИЙ
        (``id`` / F_ID), а НЕ идентификаторов объектов (``objectID``).

        Args:
            version_ids: Список идентификаторов ВЕРСИЙ объектов (``id`` / F_ID),
                извлекаемых на редактирование. Сериализуется как голый JSON-массив
                ``list[int]`` в теле запроса.
            throw_exception: Если ``True``, сервер бросит исключение при ошибке по
                любой версии; если ``False`` (по умолчанию) — проблемные элементы
                будут опущены (query ``throwException``).

        Returns:
            Словарь результата ``ObjectCheckOutVersionsResult`` со списками
            ``objects`` / ``pairVersionSources`` / ``pairVersionTargets`` (каждый —
            массив ``ObjectCheckOutVersionsItem``). Этот словарь нужно передать как
            тело в :meth:`object_rollback_check_out` для отката. Пустой словарь, если
            сервер ничего не вернул.

        Raises:
            IPSConflictError: Если какая-либо версия уже извлечена или режим ЖЦ не
                допускает редактирование (при ``throw_exception=True``).
            IPSError: При ином ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.object_check_out_versions([102550, 102551])
                try:
                    ...  # правка версий
                finally:
                    await ips.object_rollback_check_out(result)

        Notes:
            ``operationId``: ``Objects_CheckOutVersions``. Эндпоинт
            ``POST /core/api/objects/ObjectsCheckOutServerService/CheckOut``.
            Тело — голый массив ``list[int]``; ответ — ``ObjectCheckOutVersionsResult``
            (возвращается как dict без распаковки). Связанные методы:
            :meth:`object_rollback_check_out`, :meth:`object_load_descriptions`.
        """
        params: dict[str, Any] = {"throwException": str(throw_exception).lower()}
        data = await self._request(
            "post",
            "/core/api/objects/ObjectsCheckOutServerService/CheckOut",
            json=version_ids,
            params=params,
        )
        return data if isinstance(data, dict) else {}
