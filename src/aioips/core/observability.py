"""Наблюдаемость клиента IPS: лёгкий хук метрик/трейсинга вокруг каждого запроса.

Без жёсткой зависимости от OpenTelemetry: клиент вызывает пользовательский колбэк
:data:`MetricsHook` после КАЖДОЙ попытки HTTP-запроса (включая повторы). Колбэк
получает :class:`RequestMetric` и сам решает, что делать — писать метрику Prometheus,
создавать OTel-span, логировать и т.п.

Пример моста к OpenTelemetry::

    from opentelemetry import trace
    tracer = trace.get_tracer("aioips")

    def otel_hook(m: RequestMetric) -> None:
        with tracer.start_as_current_span(f"ips {m.method} {m.path}") as span:
            span.set_attribute("http.status_code", m.status or 0)
            span.set_attribute("ips.attempt", m.attempt)
            span.set_attribute("ips.duration_ms", m.duration_ms)
            if m.error:
                span.record_exception(m.error)

    async with IPSClient(config=cfg, metrics_hook=otel_hook) as ips:
        ...
"""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestMetric:
    """Сведения об одной попытке HTTP-запроса к IPS (для хука наблюдаемости).

    Attributes:
        method: HTTP-метод в нижнем регистре (``get``/``post``/…).
        path: Путь эндпоинта (без базового URL), напр. ``/core/api/objects/select``.
        status: HTTP-статус ответа или ``None``, если запрос не дошёл (сетевая ошибка).
        duration_ms: Длительность попытки в миллисекундах.
        attempt: Номер попытки, начиная с ``1`` (повторы tenacity увеличивают значение).
        error: Исключение, если попытка завершилась ошибкой/исключением, иначе ``None``.
    """

    method: str
    path: str
    status: int | None
    duration_ms: float
    attempt: int
    error: BaseException | None = None


# Колбэк наблюдаемости: вызывается синхронно после каждой попытки запроса. Должен
# быть быстрым и НЕ бросать исключений (клиент глушит исключения хука, чтобы не
# ломать сам запрос).
MetricsHook = Callable[[RequestMetric], None]
