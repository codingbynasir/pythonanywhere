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

app_name="order_billing"

urlpatterns = [
    path("order/test/<int:id>", views.getTestOrder.as_view(), name="order"),
    path('delete/test/<int:pk>', views.deleteTestOrder.as_view(), name="delete"),
    path('payment/test/<int:id>',views.testPayments.as_view(), name="payment"),
    path('payment/test/update/<int:id>', views.updateTestPayment, name="update_payment"),
    path('test/form/<int:id>', views.generateTestForm.as_view(), name="generate_form"),

    path('order/package/<int:id>', views.getPackageOrder.as_view(), name="package_order"),
    path('delete/package/<int:id>', views.deletePackageOrder.as_view(), name="delete_package_order"),
    path('payment/package/<int:id>', views.packagePayments.as_view(), name="package_payment"),
    path('payment/package/update/<int:id>', views.updatePackagePayment, name="update_package_payment"),
    path('package/form/<int:id>', views.generatePackageForm.as_view(), name="generate_package_form")
]
