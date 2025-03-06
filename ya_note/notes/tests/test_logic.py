from http import HTTPStatus

from pytils.translit import slugify

from .base_module import (
    NotesListViewTest,
    PAGE_ADD_URL,
    PAGE_SUCCESS_URL
)
from notes.forms import WARNING
from notes.models import Note


class NoteCreationTest(NotesListViewTest):
    """Тесты создания, редактирования и удаления заметок."""

    def test_logged_in_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        # Получаем начальное количество заметок.
        notes_id_before = set(Note.objects.values_list('id', flat=True))
        response = self.author_client.post(
            PAGE_ADD_URL, self.form_data
        )
        self.assertRedirects(response, PAGE_SUCCESS_URL)
        # Проверяем, что заметок на 1 больше.
        notes_id_after = set(Note.objects.values_list('id', flat=True))
        new_notes_id = notes_id_after - notes_id_before
        self.assertEqual(len(new_notes_id), 1)
        new_note_id = new_notes_id.pop()
        created_note = Note.objects.get(id=new_note_id)
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.slug, self.form_data['slug'])
        self.assertEqual(created_note.author, self.author)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        # Получаем список id до попытки создать заметку.
        note_table_before = list(Note.objects.values_list('id', flat=True))
        self.client.post(PAGE_ADD_URL, self.form_data)
        # Получаем список id после попытки создать заметку.
        note_table_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(sorted(note_table_before), sorted(note_table_after))

    def test_cannot_create_note_with_duplicate_slug(self):
        """Проверка невозможности создания двух заметок с одинаковым slug."""
        note_table_before = list(Note.objects.values_list('id', flat=True))
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            PAGE_ADD_URL, self.form_data
        )
        note_table_after = list(Note.objects.values_list('id', flat=True))
        self.assertEqual(sorted(note_table_before), sorted(note_table_after))
        self.assertFormError(
            response, 'form', 'slug', (self.form_data['slug'] + WARNING)
        )

    def test_slug_is_generated_automatically(self):
        """Проверка автоматической генерации slug при создании заметки."""
        notes_id_before = set(Note.objects.values_list('id', flat=True))
        self.form_data['slug'] = ''
        # Отправляем POST-запрос для создания заметки.
        response = self.author_client.post(PAGE_ADD_URL, self.form_data)
        self.assertRedirects(response, PAGE_SUCCESS_URL)
        notes_id_after = set(Note.objects.values_list('id', flat=True))
        new_notes_id = notes_id_after - notes_id_before
        self.assertEqual(len(new_notes_id), 1)
        new_note_id = new_notes_id.pop()
        created_note = Note.objects.get(id=new_note_id)
        self.assertEqual(created_note.slug, slugify(self.form_data['title']))
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.author, self.author)

    def test_user_can_edit_own_note(self):
        """Проверка: пользователь может редактировать свои заметки."""
        response = self.author_client.post(
            self.urls['PAGE_EDIT_URL'], self.form_data
        )
        self.assertRedirects(response, PAGE_SUCCESS_URL)
        # Получаем обновленную заметку из базы данных
        note = Note.objects.get(id=self.note.id)
        # Проверяем, что данные были успешно обновлены
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cannot_edit_other_users_note(self):
        """Проверка: пользователь не может редактировать чужие заметки."""
        response = self.reader_client.post(
            self.urls['PAGE_EDIT_URL'], self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.note.slug)

    def test_user_can_delete_own_note(self):
        """Проверка: пользователь может удалить свои заметки."""
        notes_id_before = set(Note.objects.values_list('id', flat=True))
        response = self.author_client.post(self.urls['PAGE_DELETE_URL'])
        self.assertRedirects(response, PAGE_SUCCESS_URL)
        notes_id_after = set(Note.objects.values_list('id', flat=True))
        new_notes_id = notes_id_before - notes_id_after
        self.assertEqual(len(new_notes_id), 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_user_cannot_delete_other_users_note(self):
        """Проверка: пользователь не может удалить чужие заметки."""
        response = self.reader_client.post(self.urls['PAGE_DELETE_URL'])
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        original_note = Note.objects.get(id=self.note.id)
        self.assertEqual(original_note.title, self.note.title)
        self.assertEqual(original_note.text, self.note.text)
        self.assertEqual(original_note.author, self.author)
        self.assertEqual(original_note.slug, self.note.slug)
