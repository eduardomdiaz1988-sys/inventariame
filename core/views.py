from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class BaseView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "users:login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["usuario"] = self.request.user

        return context

