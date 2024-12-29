from django.db import IntegrityError
from django.shortcuts import redirect, reverse, get_object_or_404

from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  RedirectView)

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from writer.models import Article
from client.models import Subscription, SubscriptionPlan
from client.paypal import get_access_token, cancel_subscription_papal
from client.exceptions import SubscriptionNotDeletedException


class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'client/client_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_writer:  # noqa
            return redirect(reverse(
                'writer:dashboard',
                kwargs={'writer_id': request.user.id}
            ))

        return super(ClientDashboardView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subscriptions = Subscription.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-id')

        if subscriptions.exists():
            context['sub_plan'] = subscriptions[0].subscription_plan

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
        if user.subscription.subscription_plan.name == 'standard':  # noqa
            return self.queryset.filter(is_premium=False)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Articles'
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    model = Article
    template_name = 'client/article-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edenthought | {self.get_object().title}'
        return context


class SubscriptionPlansView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    template_name = 'client/subscription-plans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Subscription Plans'
        return context


class CreateSubscriptionView(LoginRequiredMixin, RedirectView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    permanent = True
    pattern_name = 'client:dashboard'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        sub_id = self.request.GET.get('subID')
        plan_name = self.request.GET.get('plan')
        plan = get_object_or_404(SubscriptionPlan, name=plan_name)

        try:
            Subscription.objects.create(
                user=user,
                subscriber_name=user.full_name(),  # noqa
                subscription_plan=plan,
                paypal_subscription_id=sub_id,
                is_active=True
            )
            messages.success(self.request, 'Subscription created successfully!')

        except IntegrityError:
            messages.error(
                self.request,
                'Subscription not created! Invalid data has been submitted.'
            )
        except Exception as e:
            messages.error(self.request, f'Something went wrong!\n{e}')

        return super().get_redirect_url(*args, **kwargs)


class DeleteSubscriptionView(TemplateView):
    template_name = 'client/delete-subscription.html'

    @method_decorator(login_required(
        login_url='login',
        redirect_field_name='redirect_to'
    ))
    def dispatch(self, request, *args, **kwargs):
        sub_id = self.kwargs.get('subID')

        return super(DeleteSubscriptionView, self).dispatch(
            request,
            sub_id,
            *args,
            **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Delete Subscription'

        sub_id = self.kwargs.get('subID')

        # Delete subscription from PayPal
        access_token = get_access_token()

        try:
            cancel_subscription_papal(access_token, sub_id)
        except SubscriptionNotDeletedException:
            context['is_deleted'] = False

        else:
            # Delete subscription from Django (application side)
            subscription = get_object_or_404(
                Subscription,
                user=self.request.user,
                paypal_subscription_id=sub_id
            )
            subscription.delete()
            context['is_deleted'] = True

        return context
