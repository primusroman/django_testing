from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import Comment, News

User = get_user_model()


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок', text='Текст'
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def homepage_url():
    return reverse('news:home')


@pytest.fixture
def page_login_url():
    return reverse('users:login')


@pytest.fixture
def page_logout_url():
    return reverse('users:logout')


@pytest.fixture
def page_signup_url():
    return reverse('users:signup')


@pytest.fixture
def delete_url(news):
    return reverse('news:delete', args=(news.id,))


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def detail_url_with_comments(detail_url):
    return f'{detail_url}#comments'


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def redirect_delete_url(page_login_url, delete_comment_url):
    return f'{page_login_url}?next={delete_comment_url}'


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def redirect_edit_url(page_login_url, edit_comment_url):
    return f'{page_login_url}?next={edit_comment_url}'


@pytest.fixture
def all_news():
    today = datetime.today()
    return News.objects.bulk_create(News(
        title=f'Новость {index}',
        text='Просто текст.',
        date=today - timedelta(days=index)
    )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1))


@pytest.fixture
def comments(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
