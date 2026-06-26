"""Метод создания объекта IPS из записи справочника IMBASE (мутация)."""

from typing import Any

from ...core import APIManager


class ImBaseCreateObjectMixin(APIManager):
    """Реализует ``POST /core/api/imbase/object/byBase/{baseId}`` (``ImBase_CreateObject``)."""

    async def imbase_create_object(
        self: "ImBaseCreateObjectMixin",
        base_id: int,
        *,
        confirm: bool = False,
        record_id: int | None = None,
        commit_creation: bool | None = None,
        need_type: int | None = None,
    ) -> int:
        """Создаёт объект IPS из записи справочника IMBASE (МУТАЦИЯ; защищена ``confirm``).

        Порождает новый объект на основе базы (каталога) IMBASE ``base_id`` и,
        опционально, конкретной записи ``record_id``. Применяется, когда нужно
        материализовать запись справочника как полноценный объект IPS (например,
        создать объект «Материал» из строки базы материалов). Операция изменяет БД,
        поэтому по умолчанию НЕ выполняется: требуется явный ``confirm=True``, иначе
        поднимается :class:`ValueError` ещё до обращения к серверу.

        ОБРАТИМО: созданный объект можно удалить через :meth:`object_delete`
        (передав возвращённый ``objectID`` и ``confirm=True``). Если
        ``commit_creation`` оставить ``None``/``False``, создание объекта не
        зафиксировано окончательно — завершите его :meth:`object_commit_creation`
        либо откатите :meth:`object_cancel_changes`.

        Когда применять: чтобы из справочной записи IMBASE получить новый объект IPS.
        Связанные методы: :meth:`imbase_fill_object_attributes` (заполнить атрибуты
        уже существующего объекта из записи IMBASE), :meth:`imbase_add_from_im_base`
        (добавить объект из IMBASE в состав другого объекта).

        Args:
            base_id: Идентификатор базы (каталога) IMBASE, на основе которой создаётся
                объект; подставляется в путь URL.
            confirm: Подтверждение создающей операции. Без ``True`` метод не делает
                запрос (защитный гейт).
            record_id: Идентификатор записи IMBASE-таблицы, из которой берутся данные
                (query ``recordId``); ``None`` — параметр не передаётся.
            commit_creation: Сразу зафиксировать создание объекта (query
                ``commitCreation``); ``None`` — параметр не передаётся (серверный
                дефолт). При ``False``/``None`` требуется отдельный
                :meth:`object_commit_creation`.
            need_type: Идентификатор требуемого типа создаваемого объекта (query
                ``needType``); ``None`` — параметр не передаётся.

        Returns:
            Идентификатор созданного ОБЪЕКТА (``objectID``, ``int``). Ответ —
            «голое» целое (без result-обёртки); ``0`` — если сервер не вернул число.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                object_id = await ips.imbase_create_object(
                    204, record_id=1042, commit_creation=True, confirm=True
                )
                # при необходимости откатить:
                # await ips.object_delete(object_id, confirm=True)

        Notes:
            operationId ``ImBase_CreateObject``; путь
            ``POST /core/api/imbase/object/byBase/{baseId}`` (тело отсутствует, ``{}``).
            Связанные: :meth:`object_delete`, :meth:`object_commit_creation`,
            :meth:`imbase_fill_object_attributes`. См. [[ips-object-model]].
        """
        if confirm is not True:
            raise ValueError(
                "Создание объекта изменяет БД: передайте confirm=True для подтверждения"
            )
        params: dict[str, Any] = {}
        if record_id is not None:
            params["recordId"] = str(record_id)
        if commit_creation is not None:
            params["commitCreation"] = str(commit_creation).lower()
        if need_type is not None:
            params["needType"] = str(need_type)
        data = await self._request(
            "post",
            f"/core/api/imbase/object/byBase/{base_id}",
            json={},
            params=params,
        )
        return int(data) if isinstance(data, int) else 0
