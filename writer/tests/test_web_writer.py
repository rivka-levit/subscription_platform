"""
Tests for writer web pages.
Command: pytest writer\tests\test_web_writer.py --cov=writer --cov-report term-missing:skip-covered
"""

import pytest

from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_writer_dashboard_get_success(client, user_writer):
    """Test get writer dashboard page successfully."""

    client.force_login(user_writer)

    r = client.get(reverse('writer:dashboard', kwargs={'writer_id': user_writer.id}))

    assert r.status_code == 200
