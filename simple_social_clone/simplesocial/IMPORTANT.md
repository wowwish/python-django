# Migrations to Database

When migrating changes to database, keep in mind to run the migrations for all the apps of the Project
```
python manage.py migrate
python manage.py makemigrations groups
python manage.py makemigrations posts
python manage.py makemigrations accounts
python manage.py migrate
```