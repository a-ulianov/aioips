"""Метод перестановки двух файлов в файловом атрибуте объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.files.swap_files import SwapFiles


class SwapObjectFilesMixin(APIManager):
    """Реализует ``POST /core/api/files/objects/{objectId}/files/swap`` (json).

    operationId ``Files_SwapFilesInAttr``.
    """

    async def swap_object_files(
        self: "SwapObjectFilesMixin",
        object_id: int,
        body: SwapFiles,
        *,
        confirm: bool = False,
    ) -> None:
        """Переставляет два файла внутри файлового атрибута объекта (МУТИРУЮЩАЯ).

        Меняет ПОРЯДОК файлов в МНОЖЕСТВЕННОМ файловом атрибуте (``ftFile`` с
        ``is_multiple=True``): файл с позиции ``body.old_position`` перемещается
        на ``body.change_position`` и наоборот. Содержимое файлов не трогается —
        переставляется только их взаимное расположение. Применяйте, когда нужно
        задать или поправить порядок файлов в атрибуте (например, выбрать
        «первый»/основной файл в списке). Связанные методы добавления/удаления
        файлов — :meth:`add_object_file` и :meth:`delete_object_file`.

        Операция ОБРАТИМА: повторный вызов с переставленными ``old_position`` и
        ``change_position`` (то есть swap back) возвращает исходный порядок.
        Несмотря на обратимость, метод имеет защитный ``confirm``-гейт (§7):
        без ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу.

        Предусловия (ОБЯЗАТЕЛЬНО, как для прочих файловых мутаций): объект должен
        быть взят на изменение (``object_check_out``), а в ``object_id`` нужно
        передавать идентификатор РАБОЧЕЙ КОПИИ — то, что вернул
        :meth:`object_check_out` (id версии-черновика, на проде ОТРИЦАТЕЛЬНЫЙ),
        НЕ базовый ``ObjectID``. При передаче базового id объекта сервер
        отвечает 400 «выполните команду checkOut». После правки —
        ``object_check_in`` либо ``object_cancel_changes`` (см.
        ``ObjectModifyModes`` в [[ips-object-model]]). Атрибут
        ``body.attribute_id`` должен быть множественным, а ``body.blob_id`` —
        существующим файлом этого атрибута.

        Args:
            object_id: Идентификатор РАБОЧЕЙ КОПИИ объекта (результат
                :meth:`object_check_out`; на проде отрицательный), НЕ базовый
                ``ObjectID``. Уходит в путь ``{objectId}``.
            body: :class:`SwapFiles` — что переставить: ``attribute_id``
                (файловый атрибут), ``blob_id`` (адресуемый файл),
                ``old_position`` и ``change_position`` (исходный и целевой
                индексы). Сериализуется JSON-телом
                (``model_dump(mode="json", by_alias=True, exclude_none=True)``).
            confirm: Подтверждение мутации. Без ``True`` метод не делает запрос
                и поднимает :class:`ValueError` (защитный гейт §7).

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void); успехом считается
            ответ без ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибке сервера (объект не взят на изменение, атрибут
                не множественный, файл с таким ``blob_id`` не найден).

        Example:
            from aioips.schemas.files.swap_files import SwapFiles

            async with IPSClient(config=config) as ips:
                wc = await ips.object_check_out(102550)  # id рабочей копии (отриц.)
                try:
                    await ips.swap_object_files(
                        object_id=wc,  # РАБОЧАЯ КОПИЯ, не базовый ObjectID
                        body=SwapFiles(
                            attribute_id=1031,
                            blob_id=778899,
                            old_position=0,
                            change_position=1,
                        ),
                        confirm=True,
                    )
                finally:
                    await ips.object_check_in(102550)

        Notes:
            operationId ``Files_SwapFilesInAttr``; путь ``POST
            /core/api/files/objects/{objectId}/files/swap`` (тело ``SwapFiles``).
            Связанные: :meth:`add_object_file`, :meth:`delete_object_file`,
            :meth:`file_attributes`. См. [[ips-object-model]].
        """
        if confirm is not True:
            raise ValueError(
                "swap_object_files требует confirm=True: передайте confirm=True "
                "для перестановки файлов атрибута"
            )
        payload: dict[str, Any] = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        path = f"/core/api/files/objects/{object_id}/files/swap"
        await self._request("post", path, json=payload)
        return None
