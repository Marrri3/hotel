from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)

class characteristics(models.Model):
    type = models.CharField(max_length=50)
    number_of_rooms = models.IntegerField(default=1)
    number_of_beds = models.IntegerField(default=1)
    floor = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class hotel_number(models.Model):
    image = models.ImageField(upload_to='media/',unique=True)
    characteristics_id = models.ForeignKey(to=characteristics, on_delete=models.PROTECT)

class reservation(models.Model):
    date = models.DateField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    guest_id = models.ForeignKey(to=User, on_delete=models.PROTECT)
    hotel_number_id = models.ForeignKey(to=hotel_number, on_delete=models.PROTECT)


# Create your models here.
