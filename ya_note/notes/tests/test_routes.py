from http import HTTPStatus

from django.contrib.auth import get_user_model

from .base_module import NotesListViewTest

User = get_user_model()


class TestRoutes(NotesListViewTest):
    """Тестируем маршруты."""

    def test_page_availability(self):
        """Тест доступности страниц."""
        status_check_cases = (
            (self.HOMEPAGE_URL, self.client, HTTPStatus.OK),
            (self.PAGE_LOGIN_URL, self.client, HTTPStatus.OK),
            (self.PAGE_LOGOUT_URL, self.client, HTTPStatus.OK),
            (self.PAGE_SINGUP_URL, self.client, HTTPStatus.OK),
            (self.PAGE_ADD_URL, self.author_client, HTTPStatus.OK),
            (self.PAGE_SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (self.PAGE_LIST_URL, self.author_client, HTTPStatus.OK),
            (self.PAGE_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (self.PAGE_DELETE_URL, self.author_client, HTTPStatus.OK),
            (self.PAGE_EDIT_URL, self.author_client, HTTPStatus.OK),
            (self.PAGE_DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.PAGE_DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.PAGE_EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.PAGE_ADD_URL, self.client, HTTPStatus.FOUND),
            (self.PAGE_SUCCESS_URL, self.client, HTTPStatus.FOUND),
            (self.PAGE_LIST_URL, self.client, HTTPStatus.FOUND),
            (self.PAGE_DETAIL_URL, self.client, HTTPStatus.FOUND),
            (self.PAGE_DELETE_URL, self.client, HTTPStatus.FOUND),
            (self.PAGE_EDIT_URL, self.client, HTTPStatus.FOUND),
        )

        for url, user, status in status_check_cases:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тест перенаправления анонимного пользователя на страницу логина."""
        login_url = self.PAGE_LOGIN_URL
        redirect_cases = (
            (
                self.PAGE_ADD_URL,
                f'{login_url}?next={self.PAGE_ADD_URL}'
            ),
            (
                self.PAGE_EDIT_URL,
                f'{login_url}?next={self.PAGE_EDIT_URL}'
            ),
            (
                self.PAGE_DELETE_URL,
                f'{login_url}?next={self.PAGE_DELETE_URL}'
            ),
            (
                self.PAGE_LIST_URL,
                f'{login_url}?next={self.PAGE_LIST_URL}'
            ),
            (
                self.PAGE_DETAIL_URL,
                f'{login_url}?next={self.PAGE_DETAIL_URL}'
            ),
            (
                self.PAGE_SUCCESS_URL,
                f'{login_url}?next={self.PAGE_SUCCESS_URL}'
            ),
        )
        for url, expected_redirect_url in redirect_cases:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect_url)
