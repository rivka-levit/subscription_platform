from django.urls import path

from account.views import (HomeView,
                           RegisterView,
                           LoginView,
                           logout_view,
                           AccountView,
                           delete_account)

urlpatterns = [
    path('', HomeView.as_view(), name=''),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('delete-account', delete_account, name='delete_account'),
]
