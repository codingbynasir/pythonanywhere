from django.contrib import admin
from .models import patient, delete_account, shipping, verifyAccount


# Register your models here.
class patientModel(admin.ModelAdmin):
    list_display = ["__str__", "birth_date", "phone"]
    list_filter = ["sex", "height", "birth_date"]
    fieldsets = [(None, {'fields':['name','image']}),
                 ("Patient info", {'fields':['birth_date', 'weight', 'height','smoker','sex']}),
                 ("Patient Contact info", {'fields':['phone']})
                 ]
    list_per_page = 10
    search_fields = ["__str__", "phone"]

    class Meta:
        model = patient


admin.site.register(patient, patientModel)


class delete_accountModel(admin.ModelAdmin):
    list_display = ["__str__"]
    fieldsets = [
        (None, {'fields':['user']}),
        ("Why do you want to delete account?", {'fields':['reason']})]
    list_per_page = 10
    search_fields = ["__str__"]

    class Meta:
        model = delete_account


admin.site.register(delete_account, delete_accountModel)


class ShippingModel(admin.ModelAdmin):
    list_display = ["__str__"]
    list_per_page = 10
    search_fields = ["__str__"]

    class Meta:
        model = shipping


admin.site.register(shipping, ShippingModel)

class VerifyAccountModel(admin.ModelAdmin):
    list_display = ['__str__', 'hash_code']
    list_per_page = 10
    search_fields = ['__str__']
    class Meta:
        model=verifyAccount

admin.site.register(verifyAccount, VerifyAccountModel)