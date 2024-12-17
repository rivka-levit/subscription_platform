from django.db import models

from django.contrib.auth import get_user_model


class Subscription(models.Model):
    STANDARD = 'STANDARD'
    PREMIUM = 'PREMIUM'

    PAYPAL_PLAN_CHOICES = {
        STANDARD: 'Standard',
        PREMIUM: 'Premium'
    }

    subscriber_name = models.CharField(max_length=255)
    subscription_plan = models.CharField(
        max_length=255,
        choices=PAYPAL_PLAN_CHOICES,
        default=STANDARD
    )
    subscription_cost = models.DecimalField(decimal_places=2, max_digits=8)
    paypal_subscription_id = models.CharField(max_length=300)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscription',
        max_length=10,
        unique=True
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subscriber_name} - {self.subscription_plan}'
