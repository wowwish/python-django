from django.contrib import admin
from first_app.models import AccessRecord, Topic, Webpage

# Register your models here.
admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Webpage)

# Create Superuser Using:
# python manage.py createsuperuser
# python manage.py runserver
# http://127.0.0.1:8000/admin/ - Use credentials of Super User and login 
# THE ADMIN PAGE POTENTIALLY GIVES ACCESS TO THE ENTIRE WEB SITE. YOU HAVE TO KEEP THE ACCESS TO IT SAFE