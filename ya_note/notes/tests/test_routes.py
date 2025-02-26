from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тестируем маршруты."""

    @classmethod
    def setUpTestData(cls):
        """Настройка данных, общих для всех тестов класса."""
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')

        cls.notes = Note.objects.create(
            title='Покупка телефона',
            author=cls.author,
            text='Купить телефон на др жене',
            slug='buy_iPhone'
        )

        cls.urls = (
            (
                ('notes:home', None),
                ('users:login', None),
                ('users:logout', None),
                ('users:signup', None)
            ), (
                ('notes:add', None),
                ('notes:list', None),
                ('notes:success', None),
                ('notes:edit', {'slug': cls.notes.slug}),
                ('notes:detail', {'slug': cls.notes.slug}),
                ('notes:delete', {'slug': cls.notes.slug})
            )
        )

    def response_return_function(self, name=None, user=None, args=None):
        """Базовая функция, возвращающая response."""
        with self.subTest(name=name, user=user):
            url = reverse(name, kwargs=args)
            return self.client.get(url)

    def test_page_availability(self):
        """
        Тест доступности страниц.

        Проверяем, доступны ли страницы регистрации, входа и выхода
        всем пользователю.
        """
        for name, args in self.urls[0]:
            response = self.response_return_function(name)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_auth_user(self):
        """Тест доступности страниц для аутентифицированного пользователя."""
        self.client.force_login(self.author)
        for name, args in self.urls[1]:
            if not args:
                response = self.response_return_function(
                    name, user=self.author
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_page_note(self):
        """
        Тест доступности страницы отдельной заметки.

        Также проверяем, кто может удалять и редактировать заметки.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)

            for name, args in self.urls[1]:
                if args:
                    response = self.response_return_function(
                        name, user, args=args
                    )
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тест перенаправления анонимного пользователя на страницу логина."""
        for name, args in self.urls[1]:
            response = self.response_return_function(name, args=args)
            self.assertRedirects(response, response.url)
