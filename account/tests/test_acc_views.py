import pytest
from django.urls import reverse

@pytest.mark.parametrize(
    'url_name, expected',
    [('', 200), ('register', 200), ('login', 200)]
)
def test_get_page_success(url_name, expected, client):
    r = client.get(reverse(url_name))

    assert r.status_code == expected
