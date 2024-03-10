from django.db import models
from django.contrib.auth.models import User
from . constants import GENDER_TYPE

# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(default=100000,unique=True) # account no duijon user er kokhono same hobe na
    street_address = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    city = models.CharField(max_length= 100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2) 
    birth_date = models.DateField(null=True, blank=True)
    initial_borrowing_date = models.DateField(auto_now_add=True)
    phone_num = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user.first_name)

