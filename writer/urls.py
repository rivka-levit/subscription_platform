"""
URL configuration for writer app.
"""

from django.urls import path

from writer.views import (WriterDashboardView,
                          CreateArticleView,
                          MyArticlesView,
                          UpdateArticleView,
                          delete_article)

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
    path(
        '<int:writer_id>/my-articles/',
        MyArticlesView.as_view(),
        name='my_articles'
    ),
    path(
        '<int:writer_id>/update-article/<slug:slug>/',
        UpdateArticleView.as_view(),
        name='update_article'
    ),
    path(
        '<int:writer_id>/delete-article/<slug:slug>/',
        delete_article,
        name='delete_article'
    ),
]
