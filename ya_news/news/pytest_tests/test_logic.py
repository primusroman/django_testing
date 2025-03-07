from http import HTTPStatus

from django.contrib.auth import get_user_model
import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db
User = get_user_model()

FORM_DATA = {
    'text': 'Новый текст коммента'
}

BAD_TEXT_FORMS = [
    {
        'text': f'Какой-то текст, {word}, еще текст'
    } for word in BAD_WORDS
]


def test_anonymous_user_cant_create_comment(
        client, detail_url
):
    client.post(detail_url, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author, author_client, news, detail_url, detail_url_with_comments
):
    response = author_client.post(detail_url, data=FORM_DATA)
    assertRedirects(response, detail_url_with_comments)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'bad_text_forms', BAD_TEXT_FORMS,
)
def test_user_cant_use_bad_words(
        author_client, detail_url, bad_text_forms
):
    response = author_client.post(
        detail_url, data=bad_text_forms
    )
    # Проверяем, есть ли в ответе ошибка формы.
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client, delete_comment_url, detail_url_with_comments
):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, detail_url_with_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, news, delete_comment_url
):
    response = not_author_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.id).exists()
    current_comment = Comment.objects.get(pk=comment.id)
    assert current_comment.news == comment.news
    assert current_comment.author == comment.author
    assert current_comment.text == comment.text


def test_author_can_edit_comment(
        author_client, comment, edit_comment_url, detail_url_with_comments
):
    response = author_client.post(edit_comment_url, data=FORM_DATA)
    assertRedirects(response, detail_url_with_comments)
    updated_comment = Comment.objects.get(pk=comment.id)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, edit_comment_url, news
):
    response = not_author_client.post(edit_comment_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    current_comment = Comment.objects.get(pk=comment.id)
    assert current_comment.news == comment.news
    assert current_comment.author == comment.author
    assert current_comment.text == comment.text
