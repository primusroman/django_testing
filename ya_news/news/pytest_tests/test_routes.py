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
NOT_AUTHOR_CLIENT = lazy_fixture('not_author_client')
AUTHOR_CLIENT = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')
REDIRECT_EDIT_URL = lazy_fixture('redirect_edit_url')
REDIRECT_DELETE_URL = lazy_fixture('redirect_delete_url')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (EDIT_COMMENT_URL, NOT_AUTHOR_CLIENT,
         HTTPStatus.NOT_FOUND
         ),
        (EDIT_COMMENT_URL, AUTHOR_CLIENT,
         HTTPStatus.OK
         ),
        (DELETE_COMMENT_URL, NOT_AUTHOR_CLIENT,
         HTTPStatus.NOT_FOUND
         ),
        (DELETE_COMMENT_URL, AUTHOR_CLIENT,
         HTTPStatus.OK
         ),
        (HOMEPAGE_URL, CLIENT,
         HTTPStatus.OK
         ),
        (PAGE_LOGIN_URL, CLIENT,
         HTTPStatus.OK
         ),
        (PAGE_LOGOUT_URL, CLIENT,
         HTTPStatus.OK
         ),
        (PAGE_SIGNUP_URL, CLIENT,
         HTTPStatus.OK
         ),
        (DETAIL_URL, CLIENT,
         HTTPStatus.OK
         ),
        (EDIT_COMMENT_URL, CLIENT,
         HTTPStatus.FOUND
         ),
        (DELETE_COMMENT_URL, CLIENT,
         HTTPStatus.FOUND
         ),
    ),
)
def test_pages_availability_for_different_users(
        parametrized_client, url, expected_status
):
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    (
        (EDIT_COMMENT_URL, REDIRECT_EDIT_URL),
        (DELETE_COMMENT_URL, REDIRECT_DELETE_URL),
    ),
)
def test_redirects(
    client, url, expected_url
):
    assertRedirects(client.get(url), expected_url)
