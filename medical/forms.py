from django import forms
from .models import feedback, ratings, has_test, package, package_item
from order_billing.models import Test_order, Package_order


class has_testModel(forms.ModelForm):
    class Meta:
        model = Test_order
        fields = [
            "test"
        ]


class AuthorTestOrderUpdateForm(forms.ModelForm):
    test_taking_date = forms.DateField(widget=forms.SelectDateWidget)
    test_taking_time = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}))

    class Meta:
        model = Test_order
        fields = [
            "payment_status",
            "token_num",
            "verify",
            "is_completed",
            "test_taking_date",
            "test_taking_time",
            "status"
        ]


class AuthorPackageOrderUpdateForm(forms.ModelForm):
    test_taking_date = forms.DateField(widget=forms.SelectDateWidget)
    test_taking_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    class Meta:
        model = Package_order
        fields = [
            "payment_status",
            "token_num",
            "verify",
            "test_taking_date",
            "test_taking_time",
            "status"
        ]


class feedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ["comment"]


class RatingForm(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ["rating", "comments", "proof"]


class authorizeTestAdd(forms.ModelForm):
    class Meta:
        model = has_test
        fields = [
            "name",
            "delivary_in",
            "price",
            "is_home_deliverable",
            "test_details"
        ]


class authorizePackageAdd(forms.ModelForm):
    class Meta:
        model = package
        fields = [
            "name",
            "details",
            "price",
            "delivary_in",
            "remarks"
        ]


class authorizePackageItemAdd(forms.ModelForm):
    class Meta:
        model = package_item
        fields = [
            "package_name",
            "test"
        ]
