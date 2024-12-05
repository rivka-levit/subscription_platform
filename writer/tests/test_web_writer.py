"""
Tests for writer web pages.
Command: pytest writer\tests\test_web_writer.py --cov=writer --cov-report term-missing:skip-covered
"""

import pytest

from django.urls import reverse
from django.utils.text import slugify

from writer.models import Article

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'path_name,expected',
    [('writer:dashboard', 200), ('writer:create_article', 200)]
)
def test_writer_get_page_success(client, user_writer, path_name, expected):
    """Test get writer pages get successfully."""

    client.force_login(user_writer)

    r = client.get(reverse(path_name, kwargs={'writer_id': user_writer.id}))

    assert r.status_code == expected


def test_create_article_has_protected_form(client, user_writer):
    client.force_login(user_writer)

    r = client.get(reverse(
        'writer:create_article',
        kwargs={'writer_id': user_writer.id}
    ))
    assert r.status_code == 200
    assert 'article_form' in r.context
    assert 'csrf_token' in r.context


def test_create_article_form_fields_correct(client, user_writer):
    client.force_login(user_writer)
    r = client.get(reverse(
        'writer:create_article',
        kwargs={'writer_id': user_writer.id}
    ))
    page_body = str(r.content)

    assert r.status_code == 200
    assert 'for="id_title"' in page_body
    assert 'for="id_slug"' in page_body
    assert 'for="id_content"' in page_body
    assert 'type="checkbox"' in page_body
    assert 'type="submit"' in page_body


def test_create_article_post_success(client, user_writer):
    payload = {
        'title': 'Sample Article Title',
        'content': 'Sample Article Content',
    }
    client.force_login(user_writer)
    r = client.post(
        reverse('writer:create_article', kwargs={'writer_id': user_writer.id}),
        data=payload
    )
    new_article = Article.objects.filter(title=payload['title'])

    assert r.status_code == 302
    assert r['Location'] == reverse(
        'writer:dashboard',
        kwargs={'writer_id': user_writer.id}
    )
    assert new_article.exists()
    assert len(new_article) == 1