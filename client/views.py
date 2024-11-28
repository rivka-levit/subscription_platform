from django.views.generic import TemplateView


class ClientDashboardView(TemplateView):
    template_name = 'client/client_dashboard.html'
