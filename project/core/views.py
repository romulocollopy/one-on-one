from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect

from core.models import Boby
from core.forms import OneOnOneForm


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


class SaveOneOnOneView(FormMixin, View):

    form_class = OneOnOneForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('home')

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.save_object()
        return super(SaveOneOnOneView, self).form_valid(form)

    def render_to_response(self, context):
        return HttpResponse("Falhou")

class LoginView(TemplateView):
    template_name = 'login.html'

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        from django.core.urlresolvers import reverse
        logout(request)
        return HttpResponseRedirect(reverse("home"))
