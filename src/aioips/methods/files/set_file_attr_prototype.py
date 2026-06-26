"""Метод назначения прототипов файловых атрибутов объекта."""

from ...core import APIManager


class SetFileAttrPrototypeMixin(APIManager):
    """Реализует ``POST /core/api/files/objects/{objectId}/setFilePrototype``.

    operationId ``Files_SetFileAttrPrototype``.
    """

    async def set_file_attr_prototype(
        self: "SetFileAttrPrototypeMixin",
        object_id: int,
        *,
        confirm: bool = False,
    ) -> None:
        """Назначает объекту прототипы его файловых атрибутов (МУТИРУЮЩАЯ).

        Запускает на стороне сервера применение прототипов файлов к файловым
        атрибутам (``ftFile``) объекта: для атрибутов, у которых задан
        файл-прототип (см. :meth:`file_prototypes`), сервер проставляет/обновляет
        привязку прототипа. Тело запроса отсутствует — объект адресуется только
        путём. Применяйте при подготовке объекта к работе с файлами, когда нужно
        «развернуть» болванки-прототипы в его файловые атрибуты. Точечно задать
        прототип одного объекта по описанию — :meth:`set_prototype`; список
        доступных прототипов — :meth:`file_prototypes`.

        Метод изменяет состояние объекта, поэтому имеет защитный ``confirm``-гейт
        (§7): без ``confirm=True`` поднимается :class:`ValueError` ещё ДО
        обращения к серверу.

        Предусловия: операция, как прочие файловые мутации, обычно требует, чтобы
        объект был в режиме изменения (``object_check_out`` → правка →
        ``object_check_in``; см. ``ObjectModifyModes`` в объектной модели IPS).

        Args:
            object_id: Идентификатор объекта, которому назначаются прототипы
                файловых атрибутов; уходит в путь ``{objectId}``. Для надёжной
                работы передавайте идентификатор РАБОЧЕЙ КОПИИ (результат
                :meth:`object_check_out`; на проде отрицательный), а не базовый
                ``ObjectID``, иначе сервер может вернуть 400 «выполните checkOut».
            confirm: Подтверждение мутации. Без ``True`` метод не делает запрос
                и поднимает :class:`ValueError` (защитный гейт §7).

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void); успехом считается
            ответ без ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибке сервера (объект не взят на изменение, у объекта
                нет файловых атрибутов с прототипами).

        Example:
            async with IPSClient(config=config) as ips:
                wc = await ips.object_check_out(102550)
                try:
                    await ips.set_file_attr_prototype(wc, confirm=True)
                finally:
                    await ips.object_check_in(102550)

        Notes:
            operationId ``Files_SetFileAttrPrototype``; путь ``POST
            /core/api/files/objects/{objectId}/setFilePrototype`` (БЕЗ тела —
            отправляется ``json={}``, иначе сервер может вернуть 415). Связанные:
            :meth:`set_prototype`, :meth:`file_prototypes`,
            :meth:`handle_file_attributes_for_object_creation`.
            См. объектной модели IPS.
        """
        if confirm is not True:
            raise ValueError(
                "set_file_attr_prototype требует confirm=True: передайте confirm=True "
                "для назначения прототипов файловых атрибутов"
            )
        path = f"/core/api/files/objects/{object_id}/setFilePrototype"
        await self._request("post", path, json={})
        return None
