from http import HTTPStatus

from django.contrib.auth import get_user_model

from .base_module import (
    NotesListViewTest,
    HOMEPAGE_URL,
    PAGE_ADD_URL,
    PAGE_SINGUP_URL,
    PAGE_LIST_URL,
    PAGE_LOGIN_URL,
    PAGE_LOGOUT_URL,
    PAGE_SUCCESS_URL,
    REDIRECT_SUCCESS_URL,
    REDIRECT_LIST_URL,
    REDIRECT_ADD_URL,
    PAGE_EDIT_URL,
    PAGE_DETAIL_URL,
    PAGE_DELETE_URL,
    REDIRECT_EDIT_URL,
    REDIRECT_DELETE_URL,
    REDIRECT_DETAIL_URL
)

User = get_user_model()


class TestRoutes(NotesListViewTest):
    """Тестируем маршруты."""

    def test_page_availability(self):
        """Тест доступности страниц."""
        status_check_cases = (
            (HOMEPAGE_URL, self.client, HTTPStatus.OK),
            (PAGE_LOGIN_URL, self.client, HTTPStatus.OK),
            (PAGE_LOGOUT_URL, self.client, HTTPStatus.OK),
            (PAGE_SINGUP_URL, self.client, HTTPStatus.OK),
            (PAGE_ADD_URL, self.author_client, HTTPStatus.OK),
            (PAGE_SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (PAGE_LIST_URL, self.author_client, HTTPStatus.OK),
            (PAGE_ADD_URL, self.client, HTTPStatus.FOUND),
            (PAGE_SUCCESS_URL, self.client, HTTPStatus.FOUND),
            (PAGE_LIST_URL, self.client, HTTPStatus.FOUND),
            (PAGE_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (PAGE_DELETE_URL, self.author_client, HTTPStatus.OK),
            (PAGE_EDIT_URL, self.author_client, HTTPStatus.OK),
            (PAGE_DETAIL_URL, self.client, HTTPStatus.FOUND),
            (PAGE_DELETE_URL, self.client, HTTPStatus.FOUND),
            (PAGE_EDIT_URL, self.client, HTTPStatus.FOUND),
            (
                PAGE_DETAIL_URL,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                PAGE_DELETE_URL,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                PAGE_EDIT_URL,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
        )

        for url, user, status in status_check_cases:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тест перенаправления анонимного пользователя на страницу логина."""
        redirect_cases = (
            (
                PAGE_ADD_URL,
                REDIRECT_ADD_URL
            ),
            (
                PAGE_EDIT_URL,
                REDIRECT_EDIT_URL
            ),
            (
                PAGE_DELETE_URL,
                REDIRECT_DELETE_URL
            ),
            (
                PAGE_LIST_URL,
                REDIRECT_LIST_URL
            ),
            (
                PAGE_DETAIL_URL,
                REDIRECT_DETAIL_URL
            ),
            (
                PAGE_SUCCESS_URL,
                REDIRECT_SUCCESS_URL
            ),
        )
        for url, expected_redirect_url in redirect_cases:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url), expected_redirect_url
                )
