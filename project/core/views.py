from django.views.generic import ListView
from core.models import Boby


class HomeView(ListView):
    model = Boby
    context_object_name = "boby_list"
