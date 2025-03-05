from http import HTTPStatus

from pytils.translit import slugify

from .base_module import NotesListViewTest
from notes.forms import WARNING
from notes.models import Note


class NoteCreationTest(NotesListViewTest):
    """Тесты создания, редактирования и удаления заметок."""

    def test_logged_in_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        # Получаем начальное количество заметок.
        initial_number_notes = Note.objects.count()
        response = self.author_client.post(self.PAGE_ADD_URL, self.form_data)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        # Проверяем, что заметок на 1 больше.
        final_number_notes = Note.objects.count()
        self.assertEqual(final_number_notes, initial_number_notes + 1)
        new_notes = Note.objects.exclude(
            id__in=Note.objects.values_list(
                'id', flat=True)[:initial_number_notes]
        )
        print(new_notes)
        self.assertEqual(len(new_notes), 1)
        note = new_notes[0]
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        # Получаем список id до попытки создать заметку.
        note_table_before = list(Note.objects.values_list('id', flat=True))
        self.client.post(self.PAGE_ADD_URL, self.form_data)
        # Получаем список id после попытки создать заметку.
        note_table_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(note_table_before, note_table_after)

    def test_cannot_create_note_with_duplicate_slug(self):
        """Проверка невозможности создания двух заметок с одинаковым slug."""
        note_table_before = list(Note.objects.values_list('id', flat=True))
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.PAGE_ADD_URL, self.form_data)
        note_table_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(note_table_before, note_table_after)
        self.assertFormError(
            response, 'form', 'slug', (self.form_data['slug'] + WARNING)
        )

    def test_slug_is_generated_automatically(self):
        """Проверка автоматической генерации slug при создании заметки."""
        self.form_data['slug'] = ''
        # Отправляем POST-запрос для создания заметки.
        self.author_client.post(self.PAGE_ADD_URL, self.form_data)
        # Получаем созданную заметку из базы данных.
        created_note = Note.objects.get(title=self.form_data['title'])
        # Проверяем, что slug был сгенерирован автоматически.
        self.assertEqual(created_note.slug, slugify(self.form_data['title']))
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.author, self.author)

    def test_user_can_edit_own_note(self):
        """Проверка: пользователь может редактировать свои заметки."""
        original_note = Note.objects.get(slug=self.note.slug)
        response = self.author_client.post(self.PAGE_EDIT_URL, self.form_data)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        # Получаем обновленную заметку из базы данных
        note = Note.objects.get(slug=self.form_data['slug'])
        # Проверяем, что данные были успешно обновлены
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, original_note.author)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cannot_edit_other_users_note(self):
        """Проверка: пользователь не может редактировать чужие заметки."""
        original_note = Note.objects.get(slug=self.note.slug)
        response = self.reader_client.post(self.PAGE_EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, original_note.author)
        self.assertEqual(note.slug, self.note.slug)

    def test_user_can_delete_own_note(self):
        """Проверка: пользователь может удалить свои заметки."""
        self.assertTrue(Note.objects.filter(slug=self.note.slug).exists())
        response = self.author_client.post(self.PAGE_DELETE_URL)
        self.assertRedirects(response, self.PAGE_SUCCESS_URL)
        self.assertFalse(Note.objects.filter(slug=self.note.slug).exists())

    def test_user_cannot_delete_other_users_note(self):
        """Проверка: пользователь не может удалить чужие заметки."""
        response = self.reader_client.post(self.PAGE_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        original_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(original_note.title, self.note.title)
        self.assertEqual(original_note.text, self.note.text)
        self.assertEqual(original_note.author, self.author)
        self.assertEqual(original_note.slug, self.note.slug)
