"""
URL configuration for client app.
"""

from django.urls import path

from client.views import (ClientDashboardView,
                          BrowseArticlesView,
                          ArticleDetailView,
                          SubscriptionPlansView,
                          CreateSubscriptionView)

app_name = 'client'

urlpatterns = [
    path('dashboard/', ClientDashboardView.as_view(), name='dashboard'),
    path('browse-articles/', BrowseArticlesView.as_view(), name='browse-articles'),

    path(
        'subscription-plans/',
        SubscriptionPlansView.as_view(),
        name='subscription-plans'
    ),

    path('article-detail/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),

    path(
        'create-subscription/',
        CreateSubscriptionView.as_view(),
        name='create-subscription'),
]
