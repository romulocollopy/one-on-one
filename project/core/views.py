from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.models import Boby


class HomeView(ListView):
    model = Boby
    context_object_name = "boby_list"


class ProfileView(DetailView):
    template_name = "core/profile.html"
    model = Boby
    context_object_name = "boby"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user
