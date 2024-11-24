import pytest

from account.models import CustomUser


@pytest.fixture
def sample_user() -> CustomUser:
    return CustomUser.objects.create_user(
        email='sample_user@example.com',
        password='sample_password123',
        first_name='Sample First Name',
        last_name='Sample Last Name'
    )


@pytest.fixture
def user(**kwargs):
    """Fixture for creating a sample user and pass other parameters."""

    def _user_factory(**kwargs):
        payload = {
            'email': 'user@example.com',
            'password': 'test_pass123',
            'first_name': 'Sample First Name',
            'last_name': 'Sample Last Name'
        }
        if kwargs:
            payload.update(kwargs)

        return CustomUser.objects.create_user(**payload)

    return _user_factory

