from django.urls import path

from account.views import HomeView, RegisterView, LoginView, logout_view

urlpatterns = [
    path('', HomeView.as_view(), name=''),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
