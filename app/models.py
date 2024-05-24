from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=5000)

    def __str__(self):
        return self.name

class Cars(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='media')
    desc = models.TextField()
    price = models.IntegerField()
    travel = models.IntegerField()
    model_year = models.IntegerField()
    features = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=555)
    img = models.ImageField(upload_to='media')

class Team(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='media')
    designation = models.CharField(max_length=50)

class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='media')
    Profession = models.CharField(max_length=50)

class Order(models.Model):
    order = models.AutoField(primary_key=True,unique=True)
    car = models.CharField(max_length=111)
    price = models.IntegerField()
    first_name = models.CharField(max_length=111)
    last_name = models.CharField(max_length=111)
    email = models.CharField(max_length=111)
    phone = models.IntegerField()
    pickup_location = models.CharField(max_length=111)
    drop_location = models.CharField(max_length=111)
    pickup_date = models.CharField(max_length=111)
    pickup_time = models.CharField(max_length=111)
    special = models.CharField(max_length=111)

    def __str__(self):
        return self.first_name



