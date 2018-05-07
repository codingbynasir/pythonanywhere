from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class patient(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(help_text="Please upload a profile picture")
    birth_date = models.DateField()
    weight = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    choice = (("No", "No"), ("Yes", "Yes"))
    smoker = models.CharField(choices=choice, max_length=20)
    s = (("Male", "Male"), ("Female", "Female"))
    sex = models.CharField(choices=s, max_length=20)
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name.username

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.name.username})
class shipping(models.Model):
    patient=models.OneToOneField(patient, on_delete=models.CASCADE)
    city=models.CharField(max_length=50)
    area=models.CharField(max_length=50)
    address=models.TextField()
    alternative_mobile_no=models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.patient.name.get_full_name()


class delete_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reason = models.TextField(help_text="Why do you want to delete account?")

    def __str__(self):
        return self.user.username


class verifyAccount(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    hash_code=models.CharField(max_length=200)
    is_verify=models.BooleanField()
    def __str__(self):
        return self.user.username