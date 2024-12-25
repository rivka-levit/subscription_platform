from django.contrib import admin

from client.models import Subscription, SubscriptionPlan


admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
