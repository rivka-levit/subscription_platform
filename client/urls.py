"""
URL configuration for client app.
"""

from django.urls import path

from client.views import ClientDashboardView, BrowseArticlesView, ArticleDetailView

app_name = 'client'

urlpatterns = [
    path('dashboard/', ClientDashboardView.as_view(), name='dashboard'),
    path('browse-articles/', BrowseArticlesView.as_view(), name='browse-articles'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]
