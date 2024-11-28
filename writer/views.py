from django.views.generic import TemplateView


class WriterDashboardView(TemplateView):
    template_name = 'writer/writer_dashboard.html'
