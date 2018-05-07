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

app_name="medical"

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('tests/', views.getTests.as_view(), name="all_test"),
    path('test/<int:id>', views.getSingleTest.as_view(), name="signle_test"),
    path('details/<int:has_test_id>', views.testDetails.as_view(), name="test_details"),
    path('packages', views.testPackages.as_view(), name="test_packages"),
    path('package/<int:id>', views.singlePackage.as_view(), name="package_details"),
    path('hospitals', views.getHospitals.as_view(), name="all_hospitals"),
    path('hospital/<int:id>', views.singleHospital.as_view(), name="hospital_details"),
    path('search', views.search.as_view(), name="search"),




    # Authorized hospital url mapping
    path('author', views.getLoggedHospital.as_view(), name="logged_hospital"),
    path('author/test', views.ViewTestByHospital.as_view(), name="authorize_tests"),
    path('author/test/add', views.AuthorTestAdd.as_view(), name="authorize_test_add"),
    path('author/test/update/<int:id>', views.AuthorTestUpdate, name="authorize_test_update"),
    path('author/package', views.AuthorViewPackage.as_view(), name="authorize_package_view"),
    path('author/package/add', views.AuthorAddPackage.as_view(), name="authorize_package_add"),
    path('author/package/update/<int:id>', views.AuthorPackageUpdate, name="authorize_package_update"),
    path('author/package/item/add/<int:id>', views.AuthorPackItemAdd.as_view(), name="authorize_package_item_add"),
    path('author/package/item/update/<int:id>', views.AuthorPackItemEdit, name="authorize_package_item_update"),

    path('author/test/orders', views.AuthorTestOrder.as_view(), name="authorize_order"),
    path('author/package/orders', views.AuthorPackageOrder.as_view(), name="authorize_package_order"),
    path('author/test/order/<int:id>', views.AuthorTestSingleOrder.as_view(), name="authorize_single_order"),
    path('author/package/order/<int:id>', views.AuthorPackageSingleOrder.as_view(), name="authorize_package_single_order"),
    path('author/test/order/update/<int:id>', views.AuthorTestOrderUpdate, name="authorize_single_order_update"),
    path('author/package/order/update/<int:id>', views.AuthorPackageOrderUpdate, name="authorize_package_order_update"),



    # Archive pages

    path('author/test/orders/archive', views.AuthorTestOrderArchived.as_view(), name="authorize_test_order_archive"),
    path('author/package/orders/archive', views.AuthorPackageOrderArchived.as_view(), name="authorize_package_order_archive"),


    # Feedback and reviews urls mapping

    path('author/feedback', views.AuthorFeedback.as_view(), name="feedback"),
    path('author/review', views.AuthorReview.as_view(), name="review"),
]
