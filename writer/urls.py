"""
URL configuration for writer app.
"""

from django.urls import path

from writer.views import WriterDashboardView

app_name = 'writer'

urlpatterns = [
    path('<int:writer_id>/dashboard/', WriterDashboardView.as_view(), name='dashboard'),
]
