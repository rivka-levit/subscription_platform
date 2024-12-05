"""
Tests for writer web pages.
Command: pytest writer\tests\test_web_writer.py --cov=writer --cov-report term-missing:skip-covered
"""

import pytest

from django.urls import reverse

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
