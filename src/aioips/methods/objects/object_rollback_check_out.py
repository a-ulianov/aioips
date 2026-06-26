"""Метод отката пакетного извлечения версий объектов (rollback check-out)."""

from typing import Any

from ...core import APIManager


class ObjectRollbackCheckOutMixin(APIManager):
    """Реализует ``Objects_Rollback`` (откат пакетного check-out версий)."""

    async def object_rollback_check_out(
        self: "ObjectRollbackCheckOutMixin",
        check_out_result: dict[str, Any],
        *,
        throw_exception: bool = False,
    ) -> None:
        """Откатывает пакетный check-out, выполненный :meth:`object_check_out_versions`.

        Отменяет извлечение версий на редактирование, возвращая их в исходное
        состояние и снимая рабочие копии. Применяйте как обратную операцию к
        :meth:`object_check_out_versions`: передавайте ему **ровно тот словарь
        результата**, который вернул check-out (он несёт списки извлечённых версий и
        пар версий). Типичный сценарий — отмена правки в блоке ``finally``.

        ⚠️ Это МУТИРУЮЩАЯ, но восстанавливающая операция: она отменяет ранее
        сделанный (обратимый) checkout и не теряет данных самих объектов.

        Args:
            check_out_result: Результат ``ObjectCheckOutVersionsResult``, ранее
                возвращённый :meth:`object_check_out_versions` (словарь с ключами
                ``objects`` / ``pairVersionSources`` / ``pairVersionTargets``).
                Передаётся в тело запроса как есть.
            throw_exception: Если ``True``, сервер бросит исключение при ошибке
                отката; если ``False`` (по умолчанию) — ошибки по элементам
                подавляются (query ``throwException``).

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.object_check_out_versions([102550, 102551])
                try:
                    ...  # правка
                finally:
                    await ips.object_rollback_check_out(result)

        Notes:
            ``operationId``: ``Objects_Rollback``. Эндпоинт
            ``POST /core/api/objects/ObjectsCheckOutServerService/Rollback``.
            Тело — объект ``ObjectCheckOutVersionsResult`` (передаётся словарём);
            ответ — void → ``None``. Связанные методы:
            :meth:`object_check_out_versions`, :meth:`object_load_descriptions`.
        """
        params: dict[str, Any] = {"throwException": str(throw_exception).lower()}
        await self._request(
            "post",
            "/core/api/objects/ObjectsCheckOutServerService/Rollback",
            json=check_out_result,
            params=params,
        )
        return None
