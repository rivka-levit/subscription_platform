from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from django.shortcuts import render, reverse, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from writer.forms import ArticleForm


class WriterDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'writer/writer_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        return super(WriterDashboardView, self).dispatch(
            request,
            self.kwargs['writer_id'],
            *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Writer Dashboard'
        return context


class CreateArticleView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request, writer_id):  # noqa
        form = ArticleForm()
        context = {
            'article_form': form,
            'title': 'Edenthought | Create Article'
        }

        return render(request, 'writer/create_article.html', context=context)


    def post(self, request, writer_id):  # noqa
        user = get_user_model().objects.get(id=writer_id)
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = user
            article.save()

            return redirect(reverse('writer:dashboard', kwargs={'writer_id': writer_id}))

        return HttpResponse('Invalid form!')
