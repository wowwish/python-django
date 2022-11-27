# pip install Faker
import os
# Set the environment variable 'DJANGO_SETTINGS_MODULE' to the 'settings.py' file of this Project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProTwo.settings')
import django
django.setup() # Load the settings and configure Django for Standalone Usage
# Load your models from the App
from AppTwo.models import User
from faker import Faker

fakegen = Faker()

def populate(N=10):
    for entry in range(N):
        first = fakegen.unique.first_name()
        last = fakegen.unique.last_name()
        mail = fakegen.email()
        person = User.objects.get_or_create(first_name=first, last_name=last, email=mail)[0]


if __name__ == '__main__':
    print('populating script!')
    populate(20)
    print('populating complete!')