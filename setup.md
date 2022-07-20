
Reference on how to set up this backend repo from scratch


# Project
poke_project

# Requirements

python3
pipenv


# Setup

1. in root dir, ```pipenv shell``` will create virtual environment and its config artifacts ```Pipfile``` and ```Pipfile.lock```.

After step 1, run subsequent commands in virtual environment.

2. ```pipenv install django``` install django.
3. ```django-admin startproject poke_project .``` start project.

4. ```python manage.py runserver``` run server. with some port specified: ```python manage.py runserver 8000```.
5. ```python manage.py startapp pokemon``` add app.
6. In ```./poke_project/settings.py```, add new entry ```pokemon``` in array ```INSTALLED_APPS```.

Step 4. is required if network config is not set in django-admin

# Routes


# Application level

Write handlers in ```./<app>/views.py```
Write endpoints in ```./<app>/routes.py```


# Project level

## See ```./<project>/urls.py```

To hook app's URLConf to project, add ```path('<sub_path>/', include('<app>.<route_file>'))``` to ```urlpattern:URLConf```.

Example: ```path('pokemon/', include('pokemon.routes'))```