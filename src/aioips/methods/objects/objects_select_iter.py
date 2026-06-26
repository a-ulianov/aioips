"""Хелпер keyset-пагинации поверх ``objects_select`` (для больших выборок)."""

from collections.abc import AsyncIterator

from ...schemas.objects import ObjectSelectResult, SelectCondition
from .objects_select import ObjectsSelectMixin


class ObjectsSelectIterMixin(ObjectsSelectMixin):
    """Асинхронный итератор объектов с автоматической keyset-пагинацией."""

    async def objects_select_iter(
        self: "ObjectsSelectIterMixin",
        object_type_id: int,
        *,
        conditions: list[SelectCondition] | None = None,
        attribute_ids: list[int] | None = None,
        page_size: int = 1000,
        local_types_mode: bool = False,
        trash_mode: bool = False,
    ) -> AsyncIterator[ObjectSelectResult]:
        """Итерирует ВСЕ объекты выборки постранично, не держа всё в памяти.

        Обёртка над :meth:`objects_select`, автоматически проходящая keyset-пагинацию
        (курсор ``lastKeyValue`` = ``object_id`` последней записи страницы). Применяйте
        вместо одиночного :meth:`objects_select` для больших выборок (десятки тысяч
        объектов — напр. все чертежи типа), чтобы не грузить весь результат разом и не
        упираться в память/таймаут. Память постоянна (одна страница за раз).

        Алгоритм: запрашивает страницу из ``page_size`` записей; отдаёт каждую; если
        записей меньше ``page_size`` — выборка исчерпана и итерация завершается; иначе
        курсор сдвигается на ``object_id`` последней записи и берётся следующая страница.

        Args:
            object_type_id: Идентификатор ТИПА искомых объектов (``ObjectTypeID``).
            conditions: Условия фильтрации (:class:`SelectCondition`), как в
                :meth:`objects_select`. Применяются к каждой странице одинаково.
            attribute_ids: Какие атрибуты вернуть в каждой записи. ``None`` — серверный
                набор по умолчанию.
            page_size: Размер страницы (``recordCount``). По умолчанию ``1000``.
            local_types_mode: Режим локальных типов. По умолчанию ``False``.
            trash_mode: Искать в корзине. По умолчанию ``False``.

        Yields:
            :class:`ObjectSelectResult` — найденные объекты по одному, по всем страницам.

        Raises:
            IPSError: При ошибочном ответе сервера на любой странице.

        Example:
            async with IPSClient(config=config) as ips:
                count = 0
                async for obj in ips.objects_select_iter(1742, page_size=5000):
                    count += 1  # обрабатываем по одному, память не растёт
                print("всего объектов типа 1742:", count)

        Notes:
            Курсор — keyset по ``object_id`` (``lastKeyValue``), не offset (см.
            [[ips-object-model]]). Если задавать пользовательскую сортировку, для
            корректного курсора нужен ещё ``last_order_value`` — тогда используйте
            :meth:`objects_select` напрямую. Связанные методы: :meth:`objects_select`,
            :meth:`object_get`.
        """
        last_key: int | None = None
        while True:
            page = await self.objects_select(
                object_type_id,
                conditions=conditions,
                attribute_ids=attribute_ids,
                record_count=page_size,
                local_types_mode=local_types_mode,
                trash_mode=trash_mode,
                last_key_value=last_key,
            )
            for result in page:
                yield result
            if len(page) < page_size:
                return
            last_key = page[-1].object_id
