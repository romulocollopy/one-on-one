"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from project.core import views as core

urlpatterns = [
    url(r'^$', core.HomeView.as_view(), name='home'),
    url(r'^save/$', core.SaveOneOnOneView.as_view(), name='save'),
    url(r'^upload/$', core.UploadUsersView.as_view(), name='upload_users'),
    url(r'^login/$', core.LoginView.as_view(), name='login'),
    url(r'^logout/$', core.LogoutView.as_view(), name='logout'),
    url(r'^profile/$', core.CandidatesView.as_view(), name='profile'),
    # core.ProfileView.as_view()
    url(r'^social/', include('social.apps.django_app.urls',
                             namespace='social')),
    url(r'^me/$', core.CandidatesView.as_view(), name='candidates'),

    url(r'^admin/', admin.site.urls),
]
