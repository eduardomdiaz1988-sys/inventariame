from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class BaseView(LoginRequiredMixin, TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["usuario"] = self.request.user
        return context
