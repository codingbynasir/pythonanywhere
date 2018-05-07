from django.contrib import admin
from .models import hospital, test_category, diagnostic_test, has_test, package, package_item, ratings, feedback


# Register your models here.
class hospitalModel(admin.ModelAdmin):
    list_display = ["__str__", "email", "phone", "address"]
    list_filter = ["type", "division"]
    fieldsets = [('Hospital info', {'fields': ['name', 'type']}),
                 ("Contact info", {'fields': ['email', 'phone', 'address', 'zip_code', 'division']}),
                 ]
    list_per_page = 10
    search_fields = ["__str__", "email", "address", "phone", "zip_code", "division", "type"]

    class Meta:
        model = hospital


admin.site.register(hospital, hospitalModel)


class test_categoryModel(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
    list_per_page = 10
    search_fields = ["__str__", "details"]

    class Meta:
        model = test_category


admin.site.register(test_category, test_categoryModel)


class diagnostic_testModel(admin.ModelAdmin):
    list_display = ["__str__", "category"]
    list_per_page = 10
    search_fields = ["__str__", "category"]
    list_filter = ["category"]

    class Meta:
        model = diagnostic_test


admin.site.register(diagnostic_test, diagnostic_testModel)


class has_testModel(admin.ModelAdmin):
    list_display = ["__str__", "hospital", "price", "delivary_in"]
    list_per_page = 10
    search_fields = ["__str__", "hospital", "price"]
    list_filter = ["is_home_deliverable","delivary_in", "hospital"]

    class Meta:
        model = has_test


admin.site.register(has_test, has_testModel)


class packageModel(admin.ModelAdmin):
    list_display = ["__str__", "hospital", "price", "delivary_in"]
    list_per_page = 10
    search_fields = ["__str__", "hospital", "price"]
    list_filter = ["delivary_in", "price"]

    class Meta:
        model = package


admin.site.register(package, packageModel)


class package_itemModel(admin.ModelAdmin):
    list_display = ["__str__"]
    list_per_page = 10
    search_fields = ["__str__", "test"]

    class Meta:
        model = package_item


admin.site.register(package_item, package_itemModel)

class ratingsModel(admin.ModelAdmin):
    list_display = ["__str__", "rating", "comments", 'aprove']
    list_per_page = 10
    search_fields = ["__str__", "rating", "comments"]
    list_filter = ['date', 'rating', 'aprove']

    class Meta:
        model = ratings


admin.site.register(ratings, ratingsModel)


class feedbackModel(admin.ModelAdmin):
    list_display = ["__str__", "hospital", "date"]
    list_per_page = 10
    search_fields = ["__str__", "hospital", "comment"]
    list_filter = ['date', 'hospital']

    class Meta:
        model = feedback


admin.site.register(feedback, feedbackModel)