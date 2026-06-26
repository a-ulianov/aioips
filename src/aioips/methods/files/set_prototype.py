"""Метод назначения объекту файла-прототипа по описанию."""

from typing import Any

from ...core import APIManager
from ...schemas.files.prototype_info import PrototypeInfo


class SetPrototypeMixin(APIManager):
    """Реализует ``POST /core/api/files/setPrototype/{objectId}`` (json).

    operationId ``Files_SetPrototype``.
    """

    async def set_prototype(
        self: "SetPrototypeMixin",
        object_id: int,
        prototype: PrototypeInfo,
        *,
        confirm: bool = False,
    ) -> bool:
        """Назначает объекту конкретный файл-прототип по описанию (МУТИРУЮЩАЯ).

        Привязывает к объекту указанный прототип (:class:`PrototypeInfo`:
        ``prototype_id`` + при необходимости ``attribute_id``), задавая, какая
        болванка-шаблон файла относится к его файловому атрибуту (``ftFile``). В
        отличие от :meth:`set_file_attr_prototype` (разворачивает прототипы всех
        файловых атрибутов объекта без тела) здесь прототип задаётся ТОЧЕЧНО и
        ЯВНО — описанием в ``prototype``. Список доступных прототипов объекта —
        :meth:`file_prototypes`.

        Метод изменяет состояние объекта, поэтому имеет защитный ``confirm``-гейт
        (§7): без ``confirm=True`` поднимается :class:`ValueError` ещё ДО
        обращения к серверу.

        Предусловия: операция, как прочие файловые мутации, обычно требует, чтобы
        объект был в режиме изменения (``object_check_out`` → правка →
        ``object_check_in``; см. ``ObjectModifyModes`` в [[ips-object-model]]).

        Args:
            object_id: Идентификатор объекта, которому назначается прототип;
                уходит в путь ``{objectId}``. Для надёжной работы передавайте
                идентификатор РАБОЧЕЙ КОПИИ (результат :meth:`object_check_out`;
                на проде отрицательный), а не базовый ``ObjectID``, иначе сервер
                может вернуть 400 «выполните checkOut».
            prototype: :class:`PrototypeInfo` — описание прототипа: ``prototype_id``
                и ``name`` (обязательны), ``attribute_id`` (опционально — к какому
                файловому атрибуту относится). Сериализуется JSON-телом
                (``model_dump(mode="json", by_alias=True, exclude_none=True)``).
            confirm: Подтверждение мутации. Без ``True`` метод не делает запрос
                и поднимает :class:`ValueError` (защитный гейт §7).

        Returns:
            ``bool`` — ``True``, если прототип успешно назначен; ``False`` иначе.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибке сервера (объект не взят на изменение, прототип
                не найден).

        Example:
            from aioips.schemas.files.prototype_info import PrototypeInfo

            async with IPSClient(config=config) as ips:
                wc = await ips.object_check_out(102550)
                try:
                    ok = await ips.set_prototype(
                        wc,
                        PrototypeInfo(prototype_id=42, name="Чертёж PDF", attribute_id=1031),
                        confirm=True,
                    )
                finally:
                    await ips.object_check_in(102550)

        Notes:
            operationId ``Files_SetPrototype``; путь ``POST
            /core/api/files/setPrototype/{objectId}`` (тело ``PrototypeInfo``).
            Связанные: :meth:`set_file_attr_prototype`, :meth:`file_prototypes`,
            :meth:`handle_file_attributes_for_object_creation`.
            См. [[ips-object-model]].
        """
        if confirm is not True:
            raise ValueError(
                "set_prototype требует confirm=True: передайте confirm=True "
                "для назначения файла-прототипа объекту"
            )
        payload: dict[str, Any] = prototype.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
        path = f"/core/api/files/setPrototype/{object_id}"
        data = await self._request("post", path, json=payload)
        return bool(data) if data is not None else False
