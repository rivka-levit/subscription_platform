from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect
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
            return redirect('login')
        return HttpResponse(f'Invalid Form: {form.errors}')

class LoginView(View):
    def get(self, request):  # noqa
        form = AuthenticationForm()
        context = {'login_form': form}
        return render(request, 'account/login.html', context)

    def post(self, request):  # noqa
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')  # Username / Email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.is_writer:  # noqa
                    return HttpResponse('Welcome, writer!')

                return HttpResponse('Welcome, client!')

        return HttpResponse(f'Invalid Form: {form.errors}')
