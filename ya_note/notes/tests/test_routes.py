from http import HTTPStatus

from django.contrib.auth import get_user_model

from .base_module import NotesListViewTest

User = get_user_model()


class TestRoutes(NotesListViewTest):
    """Тестируем маршруты."""

    def test_page_availability(self):
        """Тест доступности страниц."""
        status_check_cases = (
            (self.urls.HOMEPAGE_URL, self.client, HTTPStatus.OK),
            (self.urls.PAGE_LOGIN_URL, self.client, HTTPStatus.OK),
            (self.urls.PAGE_LOGOUT_URL, self.client, HTTPStatus.OK),
            (self.urls.PAGE_SINGUP_URL, self.client, HTTPStatus.OK),
            (self.urls.PAGE_ADD_URL, self.author_client, HTTPStatus.OK),
            (self.urls.PAGE_SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (self.urls.PAGE_LIST_URL, self.author_client, HTTPStatus.OK),
            (self.urls.PAGE_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (self.urls.PAGE_DELETE_URL, self.author_client, HTTPStatus.OK),
            (self.urls.PAGE_EDIT_URL, self.author_client, HTTPStatus.OK),
            (self.urls.PAGE_ADD_URL, self.client, HTTPStatus.FOUND),
            (self.urls.PAGE_SUCCESS_URL, self.client, HTTPStatus.FOUND),
            (self.urls.PAGE_LIST_URL, self.client, HTTPStatus.FOUND),
            (self.urls.PAGE_DETAIL_URL, self.client, HTTPStatus.FOUND),
            (self.urls.PAGE_DELETE_URL, self.client, HTTPStatus.FOUND),
            (self.urls.PAGE_EDIT_URL, self.client, HTTPStatus.FOUND),
            (
                self.urls.PAGE_DETAIL_URL,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                self.urls.PAGE_DELETE_URL,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                self.urls.PAGE_EDIT_URL,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
        )

        for url, user, status in status_check_cases:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тест перенаправления анонимного пользователя на страницу логина."""
        login_url = self.urls.PAGE_LOGIN_URL
        redirect_cases = (
            (
                self.urls.PAGE_ADD_URL,
                f'{login_url}?next={self.urls.PAGE_ADD_URL}'
            ),
            (
                self.urls.PAGE_EDIT_URL,
                f'{login_url}?next={self.urls.PAGE_EDIT_URL}'
            ),
            (
                self.urls.PAGE_DELETE_URL,
                f'{login_url}?next={self.urls.PAGE_DELETE_URL}'
            ),
            (
                self.urls.PAGE_LIST_URL,
                f'{login_url}?next={self.urls.PAGE_LIST_URL}'
            ),
            (
                self.urls.PAGE_DETAIL_URL,
                f'{login_url}?next={self.urls.PAGE_DETAIL_URL}'
            ),
            (
                self.urls.PAGE_SUCCESS_URL,
                f'{login_url}?next={self.urls.PAGE_SUCCESS_URL}'
            ),
        )
        for url, expected_redirect_url in redirect_cases:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect_url)
