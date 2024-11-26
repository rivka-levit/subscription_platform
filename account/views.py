from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from account.forms import CreateUserForm


class HomeView(TemplateView):
    template_name = 'account/index.html'


class RegisterView(View):

    def get(self, request):  # noqa
        form = CreateUserForm()
        context = {'register_form': form}
        return render(request, 'account/register.html', context)

    def post(self, request): # noqa
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('User created successfully')
        return HttpResponse(f'Invalid Form: {form.errors}')

class LoginView(View):
    def get(self, request):  # noqa
        return render(request, 'account/login.html')