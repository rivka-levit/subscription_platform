from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'client/client_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'
