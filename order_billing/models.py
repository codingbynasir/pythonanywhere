from django.db import models
from accounts.models import patient
from medical.models import has_test, package
from datetime import datetime

# Create your models here.
class Test_order(models.Model):
    user = models.ForeignKey(patient, on_delete=models.CASCADE)
    test = models.ForeignKey(has_test, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, default="Not Paid", choices=(
        ("Not Paid", "Not paid"), ("Partially Paid", "Partially Paid"), ("Fully Paid", "Fully Paid")))
    token_num = models.CharField(max_length=100, default="", blank=True, null=True)
    verify = models.BooleanField(default=False)
    is_completed = models.CharField(max_length=20, choices=(("Yes", "Yes"), ("No", "No")), default="No")
    test_taking_date = models.DateField(blank=True, null=True, default=datetime.now().date())
    test_taking_time = models.TimeField(blank=True, null=True, default=datetime.now().time())
    choice = (
        ("Processing", "Processing"), ("On hold", "On hold"), ("Completed", "Completed"), ("Refunded", "Refunded"),
        ("Archived", "Archived"))
    status = models.CharField(max_length=100, choices=choice, default="Processing")

    def __str__(self):
        return self.user.name.username


class Test_billing(models.Model):
    order = models.OneToOneField(Test_order, on_delete=models.CASCADE)
    paid_amount = models.IntegerField()
    account_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    paid_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "(" + str(self.order.id) + ") "

    def __patient__(self):
        return self.order.user.name.get_full_name()

    def __unicode__(self):
        return self.order.test.name


class Package_order(models.Model):
    user = models.ForeignKey(patient, on_delete=models.CASCADE)
    package_name = models.ForeignKey(package, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, default="Not Paid", choices=(
        ("Not Paid", "Not paid"), ("Partially Paid", "Partially Paid"), ("Fully Paid", "Fully Paid")))
    token_num = models.CharField(max_length=100, default="", blank=True, null=True)
    verify = models.BooleanField(default=False)
    test_taking_date = models.DateField(blank=True, null=True)
    test_taking_time = models.TimeField(blank=True, null=True)
    choice = (
        ("Processing", "Processing"), ("On hold", "On hold"), ("Completed", "Completed"), ("Refunded", "Refunded"),
        ("Archived", "Archived"))
    status = models.CharField(max_length=100, choices=choice, default="Processing")

    def __str__(self):
        return self.user.name.username


class Package_billing(models.Model):
    order = models.OneToOneField(Package_order, on_delete=models.CASCADE)
    paid_amount = models.IntegerField()
    account_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    paid_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "(" + str(self.order.id) + ") "

    def __patient__(self):
        return self.order.user.name.get_full_name()

    def __unicode__(self):
        return self.order.package_name.name
