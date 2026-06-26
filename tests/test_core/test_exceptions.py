"""Тесты иерархии исключений и разбора ответа об ошибке."""

import pytest

from aioips.core.exceptions import (
    IPSAuthError,
    IPSClientError,
    IPSConflictError,
    IPSError,
    IPSForbiddenError,
    IPSNotFoundError,
    IPSServerError,
    IPSTooManyRequestsError,
    exception_from_response,
)


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (400, IPSClientError),
        (401, IPSAuthError),
        (403, IPSForbiddenError),
        (404, IPSNotFoundError),
        (409, IPSConflictError),
        (429, IPSTooManyRequestsError),
        (500, IPSServerError),
        (503, IPSServerError),
        (418, IPSError),
    ],
)
def test_status_maps_to_exception(status: int, expected: type[IPSError]):
    err = exception_from_response(status, {"title": "T", "detail": "D"})
    assert isinstance(err, expected)
    assert err.status == status
    assert err.title == "T"
    assert err.detail == "D"


def test_message_prefers_detail():
    err = exception_from_response(404, {"title": "NotFound", "detail": "нет объекта"})
    assert err.message == "нет объекта"


def test_message_falls_back_to_title_then_status():
    assert exception_from_response(404, {"title": "NotFound"}).message == "NotFound"
    assert exception_from_response(404, None).message == "HTTP 404"


def test_error_is_exception_with_readable_str():
    err = exception_from_response(500, {"detail": "сбой"})
    assert isinstance(err, Exception)
    assert "500" in str(err)
