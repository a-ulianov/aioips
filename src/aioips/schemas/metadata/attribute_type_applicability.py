"""Схема применимости типа атрибута метаданных IPS.

В swagger ответ ``IMSAttributeTypeApplicability`` описан как строковый перечисление
(``none`` / ``objectType`` / ``relationType``). НО на боевом сервере это **флаговое**
значение: сервер может вернуть КОМБИНАЦИЮ через запятую, например
``"objectType, relationType"`` (тип атрибута применяется и к объектам, и к связям).
Поэтому схема обёрнута в ``RootModel[str]`` (принимает любую строку, не падает на
комбинациях), а разобранный набор категорий доступен через свойство ``kinds``.

References:
    ``GET /core/api/metadata/attributeTypeApplicability/{id}`` — schema
    ``IMSAttributeTypeApplicability`` (флаговая строка, возвращается напрямую).
    Прод-факт: ``attributeTypeApplicability/9`` → ``"objectType, relationType"``.
"""

from enum import StrEnum

from pydantic import RootModel


class AttributeApplicabilityKind(StrEnum):
    """Категория применимости типа атрибута (член флага ``IMSAttributeTypeApplicability``).

    Определяет, к каким сущностям объектной модели может применяться тип атрибута.

    Семантика членов:
        NONE: ``none`` — тип атрибута не применяется нигде (не используется ни
            объектами, ни связями).
        OBJECT_TYPE: ``objectType`` — тип атрибута применяется для объектов
            какого-либо типа объекта.
        RELATION_TYPE: ``relationType`` — тип атрибута применяется для объектов
            какого-либо типа связи.
    """

    NONE = "none"
    OBJECT_TYPE = "objectType"
    RELATION_TYPE = "relationType"


class AttributeTypeApplicability(RootModel[str]):
    """Применимость типа атрибута: к объектам, к связям, к обоим или ни к чему.

    Обёртка над флаговым значением ``IMSAttributeTypeApplicability``. Сервер возвращает
    строку напрямую (без ``...NullableResultDto``); это может быть как одиночное
    значение (``"none"``/``"objectType"``/``"relationType"``), так и КОМБИНАЦИЯ через
    запятую (``"objectType, relationType"``). Поэтому корень — обычная строка
    (``root``), а удобный разбор на категории — свойство :attr:`kinds`.

    Когда применять: чтобы узнать, в каком контексте задействован тип атрибута —
    у объектов, у связей, и там и там, или нигде. Связанный булев предикат
    «используется ли вообще» — :meth:`attribute_is_in_use`.

    Attributes:
        root: Сырое флаговое значение применимости строкой (как вернул сервер),
            например ``"objectType, relationType"`` или ``"none"``.

    Example:
        applicability = AttributeTypeApplicability.model_validate("objectType, relationType")
        assert applicability.root == "objectType, relationType"
        assert AttributeApplicabilityKind.OBJECT_TYPE in applicability.kinds
        assert AttributeApplicabilityKind.RELATION_TYPE in applicability.kinds
    """

    @property
    def kinds(self) -> list[AttributeApplicabilityKind]:
        """Разбирает флаговую строку на список категорий применимости.

        Returns:
            Список :class:`AttributeApplicabilityKind` для каждой распознанной
            категории во флаговом значении. Нераспознанные токены игнорируются;
            для ``"none"`` или пустой строки список пуст.
        """
        result: list[AttributeApplicabilityKind] = []
        for token in self.root.split(","):
            value = token.strip()
            if not value or value == AttributeApplicabilityKind.NONE.value:
                continue
            try:
                result.append(AttributeApplicabilityKind(value))
            except ValueError:
                continue
        return result
