"""
Test models of client app.
Command: pytest client\tests\test_models_client.py --cov=client --cov-report=term-missing:skip-covered
"""

import pytest

from client.models import Subscription

pytestmark = pytest.mark.django_db


def test_create_subscription_success(sample_user):
    """Test create subscription successfully with default parameters."""

    data = {
        'subscriber_name': f'{sample_user.first_name}_{sample_user.last_name}',
        'subscription_cost': 29.90,
        'paypal_subscription_id': 'aui6rb2sd8iu45y8gf0',
        'user': sample_user
    }

    subscription = Subscription.objects.create(**data)

    for k, v in data.items():
        assert getattr(subscription, k) == v

    assert subscription.subscription_plan == 'STANDARD'
    assert subscription.is_active == False
    assert str(subscription) == (f'{subscription.subscriber_name} - '
                                 f'{subscription.subscription_plan}')


def test_create_subscription_change_plan_and_active_success(sample_user):
    """Test create subscription successfully with Premium plan
    and active True."""

    data = {
        'subscriber_name': f'{sample_user.first_name}_{sample_user.last_name}',
        'subscription_cost': 29.90,
        'paypal_subscription_id': 'aui6rb2sd8iu45y8gf0',
        'user': sample_user,
        'is_active': True,
        'subscription_plan': 'PREMIUM'
    }

    subscription = Subscription.objects.create(**data)

    assert subscription.subscription_plan == 'PREMIUM'
    assert subscription.is_active == True
