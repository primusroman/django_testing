from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class NotesListViewTest(TestCase):
    """Тестирование представления списка заметок."""

    @classmethod
    def setUpTestData(cls):
        """Настройка данных, общих для всех тестов класса."""
        cls.author = User.objects.create_user(
            username='author', password='12345'
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader = User.objects.create_user(
            username='reader', password='password2'
        )
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title='Заметка 1',
            text='Текст заметки',
            slug='slug_test',
            author=cls.author
        )

        cls.NOTE = (cls.note.slug,)

        cls.HOMEPAGE_URL = reverse('notes:home')
        cls.PAGE_LOGIN_URL = reverse('users:login')
        cls.PAGE_LOGOUT_URL = reverse('users:logout')
        cls.PAGE_SINGUP_URL = reverse('users:signup')
        cls.PAGE_ADD_URL = reverse('notes:add')
        cls.PAGE_LIST_URL = reverse('notes:list')
        cls.PAGE_SUCCESS_URL = reverse('notes:success')
        cls.PAGE_EDIT_URL = reverse('notes:edit', args=cls.NOTE)
        cls.PAGE_DETAIL_URL = reverse('notes:detail', args=cls.NOTE)
        cls.PAGE_DELETE_URL = reverse('notes:delete', args=cls.NOTE)

        cls.data = {
            'title': 'Test Title',
            'text': 'Test content',
            'slug': 'sluggg'
        }

        cls.data_without_slug = {
            'title': 'Тестовая заметка',
            'text': 'Это текст тестовой заметки.'
        }
