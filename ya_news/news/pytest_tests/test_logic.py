from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_anonymous_user_cant_create_comment(
        client, form_data, news_id
):
    url = reverse('news:detail', args=(news_id))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author, author_client, form_data, news, news_id
):
    url = reverse('news:detail', args=(news_id))
    response = author_client.post(url, data=form_data)

    assertRedirects(response, f'{url}#comments')

    assert Comment.objects.count() == 1

    comment = Comment.objects.get()

    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(
        author_client, news_id
):
    url = reverse('news:detail', args=(news_id))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    # Проверяем, есть ли в ответе ошибка формы.
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )

    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client, comment_id, news_id
):
    url = reverse('news:detail', args=(news_id))
    delete_url = reverse('news:delete', args=(comment_id))
    url_to_comments = url + '#comments'
    response = author_client.delete(delete_url)

    assertRedirects(response, url_to_comments)

    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, news_id, comment_id
):
    delete_url = reverse('news:delete', args=(comment_id))
    response = not_author_client.delete(delete_url)

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
        author_client, comment, comment_id, form_data, news_id
):
    url = reverse('news:detail', args=(news_id))
    edit_url = reverse('news:edit', args=(comment_id))
    url_to_comments = url + '#comments'
    response = author_client.post(edit_url, data=form_data)

    assertRedirects(response, url_to_comments)

    comment.refresh_from_db()

    assert comment.text == 'Новый текст коммента'


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, comment_id, form_data, news_id
):
    edit_url = reverse('news:edit', args=(comment_id))
    response = not_author_client.post(edit_url, data=form_data)

    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()

    assert comment.text == 'Текст комментария'
