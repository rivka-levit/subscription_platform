"""
URL configuration for writer app.
"""

from django.urls import path

from writer.views import WriterDashboardView, CreateArticleView

app_name = 'writer'

urlpatterns = [
    path(
        '<int:writer_id>/dashboard/',
        WriterDashboardView.as_view(),
        name='dashboard'
    ),
    path(
        '<int:writer_id>/create-article/',
        CreateArticleView.as_view(),
        name='create_article'
    ),
]
