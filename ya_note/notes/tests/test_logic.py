from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .base_module import NotesListViewTest


class NoteCreationTest(NotesListViewTest):
    """Тесты создания, редактирования и удаления заметок."""

    def test_logged_in_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        # Получаем начальное количество заметок.
        initial_number_notes = Note.objects.count()
        response = self.author_client.post(self.PAGE_ADD_URL, self.data)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        # Проверяем, что заметок на 1 больше.
        final_number_notes = Note.objects.count()
        self.assertEqual(final_number_notes, initial_number_notes + 1)
        created_note = Note.objects.get(title=self.data['title'])
        self.assertEqual(created_note.title, self.data['title'])
        self.assertEqual(created_note.text, self.data['text'])
        self.assertEqual(created_note.slug, self.data['slug'])
        self.assertEqual(created_note.author, self.author)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        # Получаем начальное количество заметок.
        initial_number_notes = Note.objects.count()
        self.client.post(self.PAGE_ADD_URL, self.data)
        # Проверяем, что количество заметок не изменилось.
        self.assertEqual(initial_number_notes, Note.objects.count())

    def test_cannot_create_note_with_duplicate_slug(self):
        """Проверка невозможности создания двух заметок с одинаковым slug."""
        initial_number_notes = Note.objects.count()
        response = self.author_client.post(self.PAGE_ADD_URL, self.data)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        response = self.author_client.post(self.PAGE_ADD_URL, self.data)
        self.assertEqual(initial_number_notes + 1, Note.objects.count())
        self.assertFormError(
            response, 'form', 'slug', (self.data['slug'] + WARNING)
        )

    def test_slug_is_generated_automatically(self):
        """Проверка автоматической генерации slug при создании заметки."""
        # Отправляем POST-запрос для создания заметки.
        self.author_client.post(self.PAGE_ADD_URL, self.data_without_slug)
        # Получаем созданную заметку из базы данных.
        created_note = Note.objects.get(title=self.data_without_slug['title'])
        # Проверяем, что slug был сгенерирован автоматически.
        expected_slug = slugify(self.data_without_slug['title'])
        self.assertEqual(created_note.slug, expected_slug)

    def test_user_can_edit_own_note(self):
        """Проверка: пользователь может редактировать свои заметки."""
        response = self.author_client.post(self.PAGE_EDIT_URL, self.data)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        # Получаем обновленную заметку из базы данных
        updated_note = Note.objects.get(slug=self.data['slug'])
        # Проверяем, что данные были успешно обновлены
        self.assertEqual(updated_note.title, self.data['title'])
        self.assertEqual(updated_note.text, self.data['text'])
        self.assertEqual(updated_note.author, self.author)
        self.assertEqual(updated_note.slug, self.data['slug'])

    def test_user_cannot_edit_other_users_note(self):
        """Проверка: пользователь не может редактировать чужие заметки."""
        response = self.reader_client.post(self.PAGE_EDIT_URL, self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        original_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(original_note.title, self.note.title)
        self.assertEqual(original_note.text, self.note.text)
        self.assertEqual(original_note.author, self.author)
        self.assertEqual(original_note.slug, self.note.slug)

    def test_user_can_delete_own_note(self):
        """Проверка: пользователь может удалить свои заметки."""
        response = self.author_client.post(self.PAGE_DELETE_URL)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(slug=self.note.slug)

    def test_user_cannot_delete_other_users_note(self):
        """Проверка: пользователь не может удалить чужие заметки."""
        response = self.reader_client.post(self.PAGE_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        original_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(original_note.title, self.note.title)
        self.assertEqual(original_note.text, self.note.text)
        self.assertEqual(original_note.author, self.author)
        self.assertEqual(original_note.slug, self.note.slug)
