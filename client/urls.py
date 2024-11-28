"""
URL configuration for client app.
"""

from django.urls import path

from client.views import ClientDashboardView

app_name = 'client'

urlpatterns = [
    path('dashboard/', ClientDashboardView.as_view(), name='dashboard'),
]
