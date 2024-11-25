from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'account/index.html'


class RegisterView(View):
    def get(self, request):
        return render(request, 'account/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'account/login.html')