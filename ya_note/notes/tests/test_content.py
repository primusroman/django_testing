from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
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
        cls.reader = User.objects.create_user(
            username='reader', password='password2'
        )

        cls.notes_first = Note.objects.create(
            title='Заметка 1', text='Текст первой заметки', author=cls.author
        )
        cls.notes_second = Note.objects.create(
            title='Заметка 2', text='Текст второй заметки', author=cls.author
        )

        cls.urls = (
            ('notes:add', None),
            ('notes:edit', {'slug': cls.notes_first.slug}),
        )

    def test_notes_list_view_context(self):
        """Проверяем, что заметки передаются в контексте object_list."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(len(response.context['object_list']), 2)

    def test_notes_list_view_permissions(self):
        """Проверяем отсутствие заметок другого пользователя."""
        self.client.force_login(self.reader)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(len(response.context['object_list']), 0)

    def test_create_and_update_note_form(self):
        """Проверяем, что на страницу создания заметки передаётся форма."""
        self.client.force_login(self.author)

        for name, args in self.urls:
            with self.subTest(name=name):
                response = self.client.get(reverse(name, kwargs=args))
                self.assertIsInstance(response.context['form'], NoteForm)
