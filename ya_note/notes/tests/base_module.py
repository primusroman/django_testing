from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

# URL, не зависящие от slug заметок.
HOMEPAGE_URL = reverse('notes:home')
PAGE_LOGIN_URL = reverse('users:login')
PAGE_LOGOUT_URL = reverse('users:logout')
PAGE_SINGUP_URL = reverse('users:signup')
PAGE_ADD_URL = reverse('notes:add')
PAGE_LIST_URL = reverse('notes:list')
PAGE_SUCCESS_URL = reverse('notes:success')
REDIRECT_SUCCESS_URL = f'{PAGE_LOGIN_URL}?next={PAGE_SUCCESS_URL}'
REDIRECT_LIST_URL = f'{PAGE_LOGIN_URL}?next={PAGE_LIST_URL}'
REDIRECT_ADD_URL = f'{PAGE_LOGIN_URL}?next={PAGE_ADD_URL}'


def generate_note_urls(note_slug):
    """Функция для генерации URL, зависящих от slug заметок."""
    PAGE_EDIT_URL = reverse('notes:edit', args=(note_slug,))
    PAGE_DETAIL_URL = reverse('notes:detail', args=(note_slug,))
    PAGE_DELETE_URL = reverse('notes:delete', args=(note_slug,))
    REDIRECT_DELETE_URL = f'{PAGE_LOGIN_URL}?next={PAGE_DELETE_URL}'
    REDIRECT_DETAIL_URL = f'{PAGE_LOGIN_URL}?next={PAGE_DETAIL_URL}'
    REDIRECT_EDIT_URL = f'{PAGE_LOGIN_URL}?next={PAGE_EDIT_URL}'

    return {
        'PAGE_EDIT_URL': PAGE_EDIT_URL,
        'PAGE_DETAIL_URL': PAGE_DETAIL_URL,
        'PAGE_DELETE_URL': PAGE_DELETE_URL,
        'REDIRECT_DELETE_URL': REDIRECT_DELETE_URL,
        'REDIRECT_DETAIL_URL': REDIRECT_DETAIL_URL,
        'REDIRECT_EDIT_URL': REDIRECT_EDIT_URL,
    }


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

        cls.urls = generate_note_urls(cls.note.slug)

        cls.form_data = {
            'title': 'Test Title',
            'text': 'Test content',
            'slug': 'sluggg'
        }
