"""Метод получения состояния метамодели (срез изменений по датам)."""

from typing import Any

from ...core import APIManager


class MetadataStateMixin(APIManager):
    """Реализует ``POST /core/api/metadata/state`` (``Metadata_GetMetadataState``)."""

    async def metadata_state(
        self: "MetadataStateMixin",
        request: dict[str, Any],
        *,
        partial_fetch_mode: bool = False,
    ) -> dict[str, Any]:
        """Возвращает состояние (срез) метамодели с учётом известных клиенту дат обновления.

        Служебный метод синхронизации локального кэша метамодели: клиент передаёт известные
        ему даты последнего обновления по разделам метаданных, а сервер возвращает полный
        срез метамодели (типы объектов/связей, атрибуты, применяемости, схемы ЖЦ, языки и
        т.д.) вместе с актуальными датами обновления. Это операция ЧТЕНИЯ: метамодель не
        изменяется, POST используется лишь для передачи словаря дат телом.

        Когда применять: при построении/обновлении клиентского кэша описаний метамодели,
        чтобы получить её состояние одним запросом. В режиме ``partial_fetch_mode`` сервер
        может вернуть только изменившееся относительно переданных дат (частичную выборку).

        Args:
            request: Тело запроса — словарь ``{ключ_раздела: дата-время-ISO}``
                (``lastUpdateDates``: известные клиенту даты последнего обновления по
                разделам). Сериализуется в JSON «как есть»; пустой dict — запросить всё.
            partial_fetch_mode: query ``partialFetchMode``. Если ``True``, сервер отдаёт
                частичный срез (только изменения относительно переданных дат); по умолчанию
                ``False`` — полный срез.

        Returns:
            Словарь по схеме ``ImsMetadataStateDto``: коллекции описаний метамодели
            (``imsObjectTypes``, ``imsRelationTypes``, ``imsAttributeTypes``,
            ``imsTypeApplicabilities``, схемы/уровни/шаги ЖЦ и др.) и ``lastUpdateDates``.
            Возвращается как ``dict[str, Any]`` (типизированная схема не вводится).
            Пустой словарь — пустой/неожиданный ответ сервера.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                state = await ips.metadata_state({})
                object_types = state.get("imsObjectTypes", [])
                print(len(object_types))

        Notes:
            operationId ``Metadata_GetMetadataState``; путь
            ``POST /core/api/metadata/state`` с query ``partialFetchMode``. Тело — объект
            ``{string: date-time}``; ответ — ``ImsMetadataStateDto`` (возвращается dict).
            См. [[ips-object-model]].
        """
        params: dict[str, Any] = {"partialFetchMode": str(partial_fetch_mode).lower()}
        data = await self._request("post", "/core/api/metadata/state", json=request, params=params)
        return data if isinstance(data, dict) else {}
