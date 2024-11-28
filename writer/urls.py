"""
URL configuration for writer app.
"""

from django.urls import path

from writer.views import WriterDashboardView

app_name = 'writer'

urlpatterns = [
    path('dashboard/', WriterDashboardView.as_view(), name='dashboard'),
]
