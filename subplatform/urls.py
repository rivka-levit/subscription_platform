"""
URL configuration for subplatform project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('account.urls')),
       path('client/', include('client.urls', namespace='client')),
       path('writer/', include('writer.urls', namespace='writer')),
]
