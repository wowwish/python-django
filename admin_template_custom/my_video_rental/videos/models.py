from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=256)
    length = models.PositiveBigIntegerField()
    release_year = models.PositiveBigIntegerField()
    def __str__(self): # Representation of the Model instances in the Admin Page View of the Model
        return self.title

class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    phone = models.PositiveBigIntegerField()
    def __str__(self): # Representation of the Model instances in the Admin Page View of the Model
        return self.first_name + ' ' + self.last_name