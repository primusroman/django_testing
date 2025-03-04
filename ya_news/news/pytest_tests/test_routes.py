from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


HOMEPAGE_URL = lazy_fixture('homepage_url')
PAGE_LOGIN_URL = lazy_fixture('page_login_url')
PAGE_LOGOUT_URL = lazy_fixture('page_logout_url')
PAGE_SIGNUP_URL = lazy_fixture('page_signup_url')
DETAIL_URL = lazy_fixture('detail_url')
EDIT_COMMENT_URL = lazy_fixture('edit_comment_url')
DELETE_COMMENT_URL = lazy_fixture('delete_comment_url')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (EDIT_COMMENT_URL, lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND
         ),
        (EDIT_COMMENT_URL, lazy_fixture('author_client'),
         HTTPStatus.OK
         ),
        (DELETE_COMMENT_URL, lazy_fixture('not_author_client'),
         HTTPStatus.NOT_FOUND
         ),
        (DELETE_COMMENT_URL, lazy_fixture('author_client'),
         HTTPStatus.OK
         ),
        (HOMEPAGE_URL, lazy_fixture('client'),
         HTTPStatus.OK
         ),
        (PAGE_LOGIN_URL, lazy_fixture('client'),
         HTTPStatus.OK
         ),
        (PAGE_LOGOUT_URL, lazy_fixture('client'),
         HTTPStatus.OK
         ),
        (PAGE_SIGNUP_URL, lazy_fixture('client'),
         HTTPStatus.OK
         ),
        (DETAIL_URL, lazy_fixture('client'),
         HTTPStatus.OK
         )
    ),
)
def test_pages_availability_for_different_users(
        parametrized_client, url, expected_status
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        (EDIT_COMMENT_URL),
        (DELETE_COMMENT_URL),
    ),
)
def test_redirects(
    client, url, page_login_url
):
    expected_url = f'{page_login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
