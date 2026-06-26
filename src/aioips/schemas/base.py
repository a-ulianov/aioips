"""Базовая модель для всех схем IPS.

IPS Web API использует ``camelCase`` в JSON. Для питоничного кода поля моделей
именуются в ``snake_case``, а сопоставление с ``camelCase`` выполняется
автоматическим генератором алиасов. Неизвестные поля игнорируются для
совместимости с будущими версиями API.
"""

from typing import Any

from pydantic import BaseModel, BeforeValidator, ConfigDict
from pydantic.alias_generators import to_camel


def _coerce_none_to_list(value: Any) -> Any:
    """Преобразует ``None`` в пустой список (IPS отдаёт ``null`` вместо ``[]``)."""
    return [] if value is None else value


EmptyListIfNone = BeforeValidator(_coerce_none_to_list)
"""Валидатор-аннотация: заменяет ``None`` на ``[]`` для списочных полей.

IPS нередко сериализует пустые коллекции как ``null``. Применяется к полям-спискам,
которые в ответах могут приходить ``null``: ``Annotated[list[X], EmptyListIfNone]``.
"""


class IPSModel(BaseModel):
    """Базовый класс схем aioips с маппингом ``snake_case`` ↔ ``camelCase``.

    Модели можно создавать как по питоническим именам полей, так и по
    оригинальным алиасам API; при сериализации запросов используйте
    ``model_dump(by_alias=True)``.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
    )
