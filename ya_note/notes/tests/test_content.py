from notes.forms import NoteForm
from .base_module import (
    NotesListViewTest,
    PAGE_ADD_URL,
    PAGE_LIST_URL,
    PAGE_EDIT_URL
)


class NotesListViewTestq(NotesListViewTest):
    """Тестирование представления списка заметок."""
    def test_notes_list_view_context(self):
        """Проверяем, что заметки передаются в контексте object_list."""
        response = self.author_client.get(PAGE_LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        note = notes.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.note.slug)

    def test_another_user_note(self):
        """Проверяем отсутствие заметок другого пользователя."""
        response = self.reader_client.get(PAGE_LIST_URL)
        self.assertNotIn(self.note,
                         response.context['object_list']
                         )

    def test_create_and_update_note_form(self):
        """Проверяем, что на страницу создания заметки передаётся форма."""
        for url in (PAGE_ADD_URL, PAGE_EDIT_URL):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
