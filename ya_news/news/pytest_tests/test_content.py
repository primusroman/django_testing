from django.conf import settings
import pytest

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_news_count(client, all_news, homepage_url):
    assert client.get(homepage_url).context[
        'object_list'
    ].count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news, homepage_url):
    news = client.get(homepage_url).context['object_list']
    assert [news.date for news in news] == sorted(
        [news.date for news in news], reverse=True
    )


def test_comments_order(client, comments, detail_url):
    news = client.get(detail_url).context['news']
    comments_date = [comment.created for comment in news.comment_set.all()]
    assert comments_date == sorted(comments_date)


def test_anonymous_client_has_no_form(client, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
