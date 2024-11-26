import pytest
from django.urls import reverse

from account.forms import CreateUserForm


@pytest.mark.parametrize(
    'url_name, expected',
    [('', 200), ('register', 200), ('login', 200)]
)
def test_get_page_success(url_name, expected, client):
    r = client.get(reverse(url_name))

    assert r.status_code == expected


@pytest.mark.django_db
def test_register_get_page_has_form(client):
    """Test register page contains form and it is CreateUserForm instance."""

    r = client.get(reverse('register'))
    form = r.context['register_form']

    assert 'register_form' in r.context
    assert isinstance(form, CreateUserForm)


@pytest.mark.django_db
def test_register_get_page_csrf(client):
    """Test register page contains csrf token."""

    r = client.get(reverse('register'))
    assert 'csrf_token' in r.context
