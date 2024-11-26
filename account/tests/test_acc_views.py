"""
Tests for views and html pages.
Command: pytest --cov=. --cov-report term-missing:skip-covered
"""

import pytest
from django.urls import reverse

from account.forms import CreateUserForm
from account.models import CustomUser


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, expected',
    [('', 200), ('register', 200), ('login', 200)]
)
def test_get_page_success(url_name, expected, client):
    r = client.get(reverse(url_name))

    assert r.status_code == expected


def test_register_get_page_has_form(client):
    """Test register page contains form and it is CreateUserForm instance."""

    r = client.get(reverse('register'))
    form = r.context['register_form']

    assert 'register_form' in r.context
    assert isinstance(form, CreateUserForm)


def test_register_get_page_csrf(client):
    """Test register page contains csrf token."""

    r = client.get(reverse('register'))
    assert 'csrf_token' in r.context


def test_register_get_page_form_fields(client):
    """Test register page contains right form fields."""

    r = client.get(reverse('register'))
    page_body = str(r.content)

    assert 'type="email"' in page_body
    assert page_body.count('type="password"') == 2
    assert 'type="checkbox"' in page_body


def test_register_post_create_user_success(client):
    """Test post request with valid data creates a new user."""

    payload = {
        'email': 'new_user@example.com',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'password1': 'test_pass123',
        'password2': 'test_pass123'
    }
    r = client.post(reverse('register'), data=payload)
    new_user = CustomUser.objects.filter(email=payload['email'])

    assert r.status_code == 302
    assert new_user.exists()


def test_register_post_invalid_fields_not_create_user(client):
    """Test post request with invalid data not create a new user."""

    payload = {
        'email': 'new_user@example.com',
        'first_name': 'First Name',
        'last_name': 'Last Name'
    }
    r = client.post(reverse('register'), data=payload)
    new_user = CustomUser.objects.filter(email=payload['email'])

    assert r.status_code == 200
    assert 'Invalid Form' in str(r.content)
    assert new_user.exists() is False


def test_login_get_render_correct_form(client):
    """Test login page renders correct form."""

    r = client.get(reverse('login'))
    page_body = str(r.content)

    assert 'login_form' in r.context
    assert 'csrf_token' in r.context
    assert 'name="username"' in page_body
    assert 'name="password"' in page_body

def test_login_post_ordinary_client(client, sample_user):
    """Test ordinary client logged in."""

    r1 = client.post(
        reverse('login'),
        data={'username': sample_user.email, 'password': 'sample_password123'}
    )

    assert r1.status_code == 200
    assert 'Welcome, client!' in str(r1.content)

    r2 = client.get(reverse(''))

    assert r2.context['user'] == sample_user


def test_login_post_writer(client, user_writer):
    """Test writer logged in."""

    r1 = client.post(
        reverse('login'),
        data={'username': user_writer.email, 'password': 'writer_password123'}
    )

    assert r1.status_code == 200
    assert 'Welcome, writer!' in str(r1.content)

    r2 = client.get(reverse(''))

    assert r2.context['user'] == user_writer


def test_login_with_invalid_data_fails(client):
    """Test login with invalid data fails."""

    r = client.post(
        reverse('login'),
        data={'username': 'some@example.com', 'password': 'some_pass_123'}
    )
    assert r.status_code == 200
    assert 'Invalid Form' in str(r.content)
