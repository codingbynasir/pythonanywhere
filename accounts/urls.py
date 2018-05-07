"""SAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('patient/<username>', views.getPatient.as_view(), name="patient"),
    path('update', views.getUpdate.as_view(), name="update_patient"),
    path('register/', views.getRegister.as_view(), name="register"),
    path('account/create', views.getAccountCreate.as_view(), name="account_create"),
    path('login/', views.getLogin.as_view(), name="login"),
    path('shipping/create', views.CreateShipping.as_view(), name="shipping_create"),
    path('shipping/update', views.updateShipping, name="shipping_update"),
    path('changepass/', views.changePass.as_view(), name="changepass"),
    path('account/delete', views.deleteAccount.as_view(), name="delete_account"),
    path('logout/', views.getLogout, name="logout"),



    path('activate/<uidb64>/<token>',views.activate, name='activate'),
]
