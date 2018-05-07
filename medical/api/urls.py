"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from .views import (HospitalApiView,
                    HospitalCreateApiView,
                    HospitalApiRetrieve,
                    HospitalApiDelete,
                    HospitalApiUpdate)

app_name="medical"
urlpatterns = [
    path('', HospitalApiView.as_view(), name="hospitalapi"),
    url(r'^create/$', HospitalCreateApiView.as_view(), name="hospitalcreateapi"),
    url(r'^hospital/(?P<id>\d+)/$', HospitalApiRetrieve.as_view(), name="hospitalapiretrieve"),
    url(r'^delete/(?P<id>[0-9]+)/$', HospitalApiDelete.as_view(), name="hospitalapidelete"),
    url(r'^update/(?P<id>[0-9]+)/$', HospitalApiUpdate.as_view(), name="hospitalapiupdate"),
    # url(r'^packages/$', views.test_packages, name="test_packages"),
    # url(r'^search/$', views.search, name="search"),
    # url(r'^package/(?P<id>[0-9]+)/$', views.single_package, name="single_package"),
]
