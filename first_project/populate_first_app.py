# pip install Faker
import os
# configure the settings for the Project you are working on (the 'settings.py' file of this Project)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
import django
django.setup() # setup the project settings

## Fake Populate Script
import random
from first_app.models import AccessRecord,Topic,Webpage
# https://faker.readthedocs.io/en/master/
from faker import Faker

fakegen = Faker()
topics = ['Search', 'Social', 'Marketplace', 'News', 'Games']
def add_topic():
    # get_or_create():
    # A convenience method for looking up an object with the given kwargs 
    # (may be empty if your model has defaults for all fields), creating one if necessary.
    # Returns a tuple of (object, created), where object is the retrieved or created object 
    # and created is a boolean specifying whether a new object was created.
    # This is meant to prevent duplicate objects from being created when requests are made in parallel, 
    # and as a shortcut to boilerplatish code. 
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t


def populate(N=5):
    for entry in range(N):
        # get the topic for the entry
        top = add_topic()
        # create the fake data for the entry
        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()
        # create the new Webpage entry (Notice that an actual Topic object is passed for Foreign Keys)
        webpg = Webpage.objects.get_or_create(topic=top, url=fake_url,name=fake_name)[0]
        # create a fake AccessRecord for that webpage (Notice that an actual Webpage object is passed for Foreign Key)
        acc_rec = AccessRecord.objects.get_or_create(name=webpg, date=fake_date)[0]


if __name__ == '__main__':
    print('populating script!')
    populate(20)
    print('populating complete!')


# CHECK POPULATED MODELS:
# python manage.py runserver
# http://127.0.0.1:8000/admin/