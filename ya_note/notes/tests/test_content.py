from notes.forms import NoteForm
from .base_module import NotesListViewTest


class NotesListViewTestq(NotesListViewTest):
    """Тестирование представления списка заметок."""
    def test_notes_list_view_context(self):
        """Проверяем, что заметки передаются в контексте object_list."""
        response = self.author_client.get(self.PAGE_LIST_URL)
        notes_in_context = list(response.context['object_list'])
        self.assertIn(self.note, notes_in_context)

        self.assertEqual(notes_in_context[0].title, self.note.title)
        self.assertEqual(notes_in_context[0].text, self.note.text)
        self.assertEqual(notes_in_context[0].author, self.note.author)
        self.assertEqual(notes_in_context[0].slug, self.note.slug)

    def test_another_user_note(self):
        """Проверяем отсутствие заметок другого пользователя."""
        response = self.reader_client.get(self.PAGE_LIST_URL)
        self.assertNotIn(self.note,
                         list(response.context['object_list'])
                         )

    def test_create_and_update_note_form(self):
        """Проверяем, что на страницу создания заметки передаётся форма."""
        for url in (self.PAGE_ADD_URL, self.PAGE_EDIT_URL):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
