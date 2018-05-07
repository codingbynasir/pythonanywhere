from .models import Test_order, Test_billing, Package_billing
from django.contrib.auth.forms import forms


class TestBillingForm(forms.ModelForm):
    class Meta:
        model= Test_billing
        fields=[
            "account_number",
            "paid_amount",
            "transaction_id"
        ]


class PackageBillingForm(forms.ModelForm):
    class Meta:
        model= Package_billing
        fields=[
            "account_number",
            "paid_amount",
            "transaction_id"
        ]