from django.contrib import admin
from .models import Test_order, Package_order, Test_billing, Package_billing


# Register your models here.
class TestOrderModel(admin.ModelAdmin):
    list_display = ["pk", "__str__", "test", "test_taking_time"]
    list_per_page = 10
    list_display_links = ["__str__"]
    list_filter = ["status", "payment_status", "verify", "is_completed"]

    class Meta:
        model = Test_order


admin.site.register(Test_order, TestOrderModel)


class TestBillingModel(admin.ModelAdmin):
    list_display = ["__str__","__patient__", "__unicode__", "account_number", "transaction_id", "paid_amount", "paid_on"]
    list_per_page = 10
    search_fields = ["__str__", "transaction_id", "account_number"]

    class Meta:
        model = Test_billing


admin.site.register(Test_billing, TestBillingModel)


class PackageOrderModel(admin.ModelAdmin):
    list_display = ["pk", "__str__", "package_name", "test_taking_time", "status"]
    list_per_page = 10
    list_display_links = ["__str__"]
    list_filter = ["status", "verify","payment_status"]

    class Meta:
        model = Package_order


admin.site.register(Package_order, PackageOrderModel)


class PackageBillingModel(admin.ModelAdmin):
    list_display = ["__str__","__patient__", "__unicode__", "account_number", "transaction_id", "paid_amount", "paid_on"]
    list_per_page = 10
    search_fields = ["__str__", "transaction_id", "account_number"]

    class Meta:
        model = Package_billing


admin.site.register(Package_billing, PackageBillingModel)
