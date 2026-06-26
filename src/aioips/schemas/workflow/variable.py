"""Схема переменной процесса IPS.

References:
    ``GET /core/api/wfVariables/{activityId}/loadVariables`` — массив ``VariableDto``.
"""

from pydantic import Field

from ..base import IPSModel


class Variable(IPSModel):
    """Переменная процесса (workflow), доступная на активности.

    Переменные процесса хранят данные, передаваемые между шагами маршрута: входные
    параметры активности, результаты, глобальные значения экземпляра процесса.
    Возвращается методом :meth:`wf_variables`. Тип значения переменной описывается
    строкой ``variable_type`` (``VarType``: ``string``/``integer``/``float``/
    ``dateTime``/``stringList``/``participantList``/``boolean``/``archive``/``text``/
    ``unknown``).

    Attributes:
        variable_name: Системное имя переменной (уникально в контексте процесса).
        variable_id: Числовой идентификатор переменной.
        variable_type: Тип значения переменной (``VarType`` в строковом виде).
        short_name: Краткое (отображаемое) имя переменной; может отсутствовать.
    """

    variable_name: str = Field(description="Системное имя переменной")
    variable_id: int = Field(description="Идентификатор переменной")
    variable_type: str = Field(description="Тип значения переменной (VarType)")
    short_name: str | None = Field(default=None, description="Краткое имя переменной")
