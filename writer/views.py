from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class WriterDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'writer/writer_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = {'title': 'Edenthought | Writer Dashboard'}
        return context
