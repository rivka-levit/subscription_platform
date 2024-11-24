"""
Tests for user account model.
Command: pytest --cov=. --cov-report term-missing:skip-covered
"""

import pytest

from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


def test_create_user_success():
    """Test creating a new user account successfully."""

    payload = {
        'email': 'test_user@example.com',
        'password': 'test_pass123',
        'first_name': 'Sample First Name',
        'last_name': 'Sample Last Name'
    }

    user = get_user_model().objects.create_user(**payload)

    assert user.check_password(payload['password']) == True
    assert user.email == payload['email']
    assert user.first_name == payload['first_name']
    assert user.last_name == payload['last_name']
    assert user.is_active is True

    for k in ('is_staff', 'is_writer'):
        assert getattr(user, k) == False


def test_user_model_str_method(sample_user):
    """Test string representation of user model."""

    assert str(sample_user) == sample_user.email


def test_create_superuser_success():
    """Test creating a new superuser account successfully."""

    payload = {
        'email': 'test_superuser@example.com',
        'password': 'test_pass123',
        'first_name': 'Sample First Name',
        'last_name': 'Sample Last Name'
    }

    superuser = get_user_model().objects.create_superuser(**payload)

    assert superuser.is_superuser is True
    assert superuser.is_staff is True


def test_create_user_without_email_fails(user):
    """Test creating a new user account without email raises error."""

    with pytest.raises(ValueError):
        user(email=None)
