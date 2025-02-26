from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

import pytest

pytestmark = pytest.mark.django_db


def test_news_count(client, all_news):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, create_comment, news_id):
    response = client.get(reverse('news:detail', args=news_id))
    news = response.context['news']
    all_timestamps = [comment.created for comment in news.comment_set.all()]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client, news_id):
    detail_url = reverse('news:detail', args=(news_id))
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news_id):
    detail_url = reverse('news:detail', args=(news_id))
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
