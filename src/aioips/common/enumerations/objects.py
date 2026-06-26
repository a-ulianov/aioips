"""Перечисления, относящиеся к объектам IPS."""

from enum import StrEnum


class ObjectModifyMode(StrEnum):
    """Режим, в котором допускается правка атрибутов версии (``ObjectModifyModes``).

    Возвращается ядром IPS для текущего объекта и зависит от типа объекта И
    текущего шага его жизненного цикла. Определяет, можно ли менять атрибуты
    и какой процедурой. Проверяй перед записью (S3/S4-методы): прямая правка
    допустима только в ``IN_BASE``; иначе нужен цикл ``checkOut`` → править →
    ``checkIn`` либо создание новой версии.

    Семантика членов:
        IN_BASE: ``inBase`` — правка прямо в базовой версии без извлечения.
        CHECKOUT: ``checkout`` — править можно только после извлечения (checkout).
        CREATE_VERSION: ``createVersion`` — правка требует создания новой версии.
        CANT_MODIFY: ``cantModify`` — редактирование запрещено.

    References:
        Цикл редактирования — [[ips-object-model]] (раздел «Редактирование»).
    """

    IN_BASE = "inBase"
    CHECKOUT = "checkout"
    CREATE_VERSION = "createVersion"
    CANT_MODIFY = "cantModify"
