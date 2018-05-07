from django.db import models
from accounts.models import patient
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class test_category(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return self.name


class diagnostic_test(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(test_category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class hospital(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    choice = (("Clinic", "Clinic"), ("Medical college", "Medical college"), ("Diagnostic center", "Diagnostic center"),
              ("Hospital", "Hospital"), ("Check up center", "Check up center"))
    type = models.CharField(choices=choice, max_length=200, default="Hospital")
    email = models.EmailField(max_length=200, default="")
    phone = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    div = (("Dhaka", "Dhaka"), ("Barishal", "Barishal"), ("Dinajput", "Dinajput"), ("Chittagong", "Chittagong"),
           ("Khulna", "Khulna"), ("Rajshahi", "Rajshahi"), ("Rangpur", "Rangpur"))
    division = models.CharField(choices=div, max_length=50)

    def __str__(self):
        return self.name.get_full_name()


class has_test(models.Model):
    name = models.ForeignKey(diagnostic_test, on_delete=models.CASCADE)
    hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)
    test_details = models.TextField(default=None)
    price = models.IntegerField()
    delivary_in = models.IntegerField()
    is_home_deliverable = models.BooleanField(default=False)

    def __str__(self):
        return self.name.name

    def get_single_url(self):
        return reverse('medical:test_details', kwargs={"has_test_id": self.id})


class package(models.Model):
    name = models.CharField(max_length=200)
    hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)
    details = models.TextField()
    price = models.IntegerField()
    delivary_in = models.IntegerField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class package_item(models.Model):
    package_name = models.ForeignKey(package, on_delete=models.CASCADE)
    test = models.ManyToManyField(diagnostic_test)

    def __str__(self):
        return self.package_name.name


class ratings(models.Model):
    user = models.ForeignKey(patient, on_delete=models.CASCADE)
    test = models.ForeignKey(has_test, on_delete=models.CASCADE)
    r = (("Bad", "Bad"), ("Average", "Average"), ("Good", "Good"), ("Best", "Best"), ("Excellent", "Excellent"))
    rating = models.CharField(choices=r, max_length=15)
    comments = models.TextField()
    proof = models.ImageField()
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    aprove=models.BooleanField(default=False)

    def __str__(self):
        return self.test.name.name


class feedback(models.Model):
    user = models.ForeignKey(patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.user.name.username
