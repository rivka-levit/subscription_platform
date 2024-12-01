"""
Tests for writer app models.
Command: pytest writer\tests\test_models_writer.py --cov=writer --cov-report term-missing:skip-covered
All tests command: pytest --cov=. --cov-report term-missing:skip-covered
"""

import pytest

from django.utils.text import slugify
from django.db.utils import IntegrityError

from writer.models import Article

pytestmark = pytest.mark.django_db


def test_create_article_pass(user_writer):
    """Test creating an article successfully."""

    data = {
        'title': 'Test title',
        'content': 'Test content',
        'author': user_writer,
    }

    article = Article.objects.create(**data)

    assert article.title == data['title']
    assert article.content == data['content']
    assert article.author == user_writer
    assert str(article) == data['title']
    assert article.slug == slugify(data['title'])


def test_create_article_with_repeating_slug_fails(user_writer):
    """Test creating an article with repeating slug fails."""

    data = {
        'title': 'Test title',
        'content': 'Test content',
        'author': user_writer,
    }

    Article.objects.create(**data)

    with pytest.raises(IntegrityError):
        Article.objects.create(**data)
