from django.db import models

# https://docs.djangoproject.com/en/4.1/topics/db/models/

# Create your models here.
# Each Class corresponds to a Database Table.
# Django can then create the actual Database Tables with a simple command 'python manage.py migrate'
# We can register the changes to our app after the tables are created 
# using 'python manage.py makemigrations first_app'
# We then migrate one more time using 'python manage.py migrate'
# We can then use the shell from the manage.py file to play around with the models.

# In order to use the convenient Admin interface with the models, we need to register them to our application's 
# 'admin.py' file. Then, we can use the Django's Admin interface to interact with the database.
# In order to fully use the database and the admin features of Django, we need to create a "superuser", providing
# a name, email and password
# We will use a library called Faker to populate our Models with fake data

class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)
    def __str__(self): # Method to print an instance of the Model as a string
        return self.top_name


class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)
    def __str__(self):
        return self.name


class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return str(self.date)

# Create the Models for your App:
# python manage.py migrate
# python manage.py makemigrations first_app
# python manage.py migrate

# Interact with the created Models:
# python manage.py shell
# from first_app.models import Topic
# print(Topic.objects.all()) - QuerySet similar to SQL queries
# t = Topic(top_name='Social Network')
# t.save()
# print(Topic.objects.all())
# quit()