"""Метод правки сохранённой поисковой схемы (выборки) IPS (мутация)."""

from typing import Any

from ...core import APIManager


class EditSearchSchemeMixin(APIManager):
    """Реализует ``POST /core/api/searchSchemes/{objectId}/edit`` (``SearchSchemes_Edit``)."""

    async def edit_search_scheme(
        self: "EditSearchSchemeMixin",
        object_id: int,
        request: dict[str, Any],
        *,
        confirm: bool = False,
    ) -> bool:
        """Перезаписывает сохранённую поисковую схему (выборку) по идентификатору объекта (МУТАЦИЯ).

        Поисковая схема — именованная конфигурация поиска объектов (направление обхода
        связей, правило версий, типы искомых объектов, выводимые колонки, привязка к
        ролям). Метод записывает новое содержимое схемы (``SearchSchemaDto``) для
        существующего объекта схемы. Это операция ЗАПИСИ, изменяющая серверное состояние.

        Когда применять: при программном изменении параметров готовой выборки (колонок,
        правила версий, набора типов). Прочитать текущую схему можно методом
        :meth:`search_scheme` по тому же идентификатору объекта.

        Предусловие по id-пространству: ``object_id`` — идентификатор ОБЪЕКТА поисковой
        схемы (``objectID`` / F_OBJECT_ID), а не идентификатор её версии.

        Обратимость: операция ОБРАТИМА по схеме write-same-back — прочитайте схему через
        :meth:`search_scheme`, сохраните её и для отката запишите обратно этим методом.

        Защита: меняет схему на сервере, поэтому защищена ``confirm`` — без ``confirm=True``
        поднимается :class:`ValueError` ещё ДО обращения к серверу.

        Args:
            object_id: Идентификатор объекта поисковой схемы (``objectID`` / F_OBJECT_ID),
                которую нужно отредактировать (path-параметр ``objectId``).
            request: Тело схемы — словарь ``SearchSchemaDto`` (ключи ``camelCase``, как
                его отдаёт :meth:`search_scheme`). Передаётся телом запроса
                (``json=request``) без преобразований.
            confirm: Подтверждение операции записи. Без ``True`` запрос НЕ выполняется.

        Returns:
            ``True``, если сервер подтвердил успешную правку схемы; ``False`` — если
            изменение не применено (сервер вернул ``false``).

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (в т.ч. 404, если схема не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                scheme = await ips.search_scheme(102550)  # objectID схемы
                body = scheme.model_dump(by_alias=True)
                ok = await ips.edit_search_scheme(102550, body, confirm=True)

        Notes:
            operationId ``SearchSchemes_Edit``; путь
            ``POST /core/api/searchSchemes/{objectId}/edit``. Тело — ``SearchSchemaDto``
            (``json=request``). Ответ — ``boolean``.
        """
        if confirm is not True:
            raise ValueError(
                "edit_search_scheme перезаписывает поисковую схему (меняет выборку); "
                "передайте confirm=True",
            )
        data = await self._request(
            "post", f"/core/api/searchSchemes/{object_id}/edit", json=request
        )
        return bool(data)
