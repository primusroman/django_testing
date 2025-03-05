from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class UrlsForTests:
    """Класс для хранения всех URL."""

    def __init__(self, note_slug):
        self.HOMEPAGE_URL = reverse('notes:home')
        self.PAGE_LOGIN_URL = reverse('users:login')
        self.PAGE_LOGOUT_URL = reverse('users:logout')
        self.PAGE_SINGUP_URL = reverse('users:signup')
        self.PAGE_ADD_URL = reverse('notes:add')
        self.PAGE_LIST_URL = reverse('notes:list')
        self.PAGE_SUCCESS_URL = reverse('notes:success')
        self.PAGE_EDIT_URL = reverse('notes:edit', args=(note_slug,))
        self.PAGE_DETAIL_URL = reverse('notes:detail', args=(note_slug,))
        self.PAGE_DELETE_URL = reverse('notes:delete', args=(note_slug,))


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

        cls.urls = UrlsForTests(cls.note.slug)

        # cls.HOMEPAGE_URL = reverse('notes:home')
        # cls.PAGE_LOGIN_URL = reverse('users:login')
        # cls.PAGE_LOGOUT_URL = reverse('users:logout')
        # cls.PAGE_SINGUP_URL = reverse('users:signup')
        # cls.PAGE_ADD_URL = reverse('notes:add')
        # cls.PAGE_LIST_URL = reverse('notes:list')
        # cls.PAGE_SUCCESS_URL = reverse('notes:success')
        # cls.PAGE_EDIT_URL = reverse('notes:edit', args=(cls.note.slug,))
        # cls.PAGE_DETAIL_URL = reverse('notes:detail', args=(cls.note.slug,))
        # cls.PAGE_DELETE_URL = reverse('notes:delete', args=(cls.note.slug,))

        cls.form_data = {
            'title': 'Test Title',
            'text': 'Test content',
            'slug': 'sluggg'
        }
