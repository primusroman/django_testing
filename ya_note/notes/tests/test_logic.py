from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note


class NoteCreationTest(TestCase):
    """Тесты создания заметок."""

    @classmethod
    def setUpTestData(cls):
        """Настройка данных, общих для всех тестов класса."""
        cls.user = User.objects.create_user(
            username='testuser', password='12345'
        )

        cls.data = {
            'title': 'Test Title',
            'text': 'Test content',
            'slug': 'test-slug'
        }

        cls.duplicate_note_data = {
            'title': 'Another Note',
            'text': 'This is another note.',
            'slug': 'test-slug',
        }

    def test_logged_in_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('notes:add'), self.data)
        self.assertRedirects(response, reverse('notes:success'))
        # Проверяем, что заметка создана в базе данных
        self.assertTrue(Note.objects.filter(
            title='Test Title',
            text='Test content',
            slug='test-slug',
            author=self.user
        ).exists())

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        self.client.post(reverse('notes:add'), self.data)
        comments_count = Note.objects.count()

        self.assertEqual(comments_count, 0)

    def test_cannot_create_note_with_duplicate_slug(self):
        """Проверка невозможности создания двух заметок с одинаковым slug."""
        self.client.force_login(self.user)
        self.client.post(reverse('notes:add'), self.data)
        self.client.post(reverse('notes:add'), self.duplicate_note_data)

        self.assertEqual(Note.objects.count(), 1)

    def test_slug_is_generated_automatically(self):
        """Проверка автоматической генерации slug при создании заметки."""
        note_title = 'Тестовая заметка'
        note = Note.objects.create(
            title=note_title,
            text='Это текст тестовой заметки.',
            author=self.user
        )
        expected_slug = slugify(note_title)

        self.assertEqual(note.slug, expected_slug)


class NotePermissionsTest(TestCase):
    """Тесты редактирования и удаления заметок."""

    @classmethod
    def setUpTestData(cls):
        """Настройка данных, общих для всех тестов класса."""
        cls.user1 = User.objects.create_user(
            username='user1', password='12345'
        )
        cls.user2 = User.objects.create_user(
            username='user2', password='12345'
        )

        cls.note1 = Note.objects.create(
            title='Note by User1',
            text='This is a note created by user1.',
            slug='note-by-user1',
            author=cls.user1
        )

    def test_user_can_edit_own_note(self):
        """Проверка: пользователь может редактировать свои заметки."""
        self.client.force_login(self.user1)

        # Данные для обновления заметки
        updated_data = {
            'title': 'Updated Note by User1',
            'text': 'This note has been updated.',
            'slug': 'updated-note-by-user1'
        }

        response = self.client.post(
            reverse(
                'notes:edit', kwargs={'slug': self.note1.slug}
            ),
            updated_data
        )

        self.assertRedirects(response, reverse('notes:success'))
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, updated_data['title'])

    def test_user_cannot_edit_other_users_note(self):
        """Проверка: пользователь не может редактировать чужие заметки."""
        self.client.force_login(self.user2)

        updated_data = {
            'title': 'Attempt to Update Note by User2',
            'text': 'qweqeqe',
            'slug': 'attempt-to-update-note-by-user2'
        }

        response = self.client.post(
            reverse(
                'notes:edit', kwargs={'slug': self.note1.slug}
            ),
            updated_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note1.refresh_from_db()
        self.assertNotEqual(self.note1.title, updated_data['title'])

    def test_user_can_delete_own_note(self):
        """Проверка: пользователь может удалить свои заметки."""
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse('notes:delete', kwargs={'slug': self.note1.slug})
        )

        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_delete_other_users_note(self):
        """Проверка: пользователь не может удалить чужие заметки."""
        self.client.force_login(self.user2)

        response = self.client.post(reverse(
            'notes:delete', kwargs={'slug': self.note1.slug})
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
