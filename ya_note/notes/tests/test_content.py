from notes.forms import NoteForm
from .base_module import (
    NotesListViewTest,
    PAGE_ADD_URL,
    PAGE_LIST_URL,
)


class NotesListViewTestq(NotesListViewTest):
    """Тестирование представления списка заметок."""
    def test_notes_list_view_context(self):
        """Проверяем, что заметки передаются в контексте object_list."""
        response = self.author_client.get(PAGE_LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        notes = next(
            (note for note in notes if note.pk == self.note.pk),
            None
        )
        self.assertEqual(notes.title, self.note.title)
        self.assertEqual(notes.text, self.note.text)
        self.assertEqual(notes.author, self.note.author)
        self.assertEqual(notes.slug, self.note.slug)

    def test_another_user_note(self):
        """Проверяем отсутствие заметок другого пользователя."""
        response = self.reader_client.get(PAGE_LIST_URL)
        self.assertNotIn(self.note,
                         response.context['object_list']
                         )

    def test_create_and_update_note_form(self):
        """Проверяем, что на страницу создания заметки передаётся форма."""
        for url in (PAGE_ADD_URL, self.urls['PAGE_EDIT_URL']):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
