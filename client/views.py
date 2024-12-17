from django.shortcuts import redirect, reverse

from django.views.generic import TemplateView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from writer.models import Article


class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'client/client_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_writer:
            return redirect(reverse(
                'writer:dashboard',
                kwargs={'writer_id': request.user.id}
            ))

        return super(ClientDashboardView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Dashboard'
        return context


class BrowseArticlesView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'client/browse-articles.html'

    queryset = Article.objects.all().order_by('-date_posted')
    context_object_name = 'articles'

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'subscription') or not user.subscription:  # noqa
            return None
        if user.subscription.subscription_plan == 'STANDARD':  # noqa
            return self.queryset.filter(is_premium=False)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Articles'
        return context
