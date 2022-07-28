
Reference on how to set up this backend repo from scratch


# Project
poke_project

# Requirements

python 3.8
pipenv
sqlite3

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


## Application level

Write handlers in ```./<app>/views.py```
Write endpoints in ```./<app>/routes.py```


## Project level

### See ```./<project>/urls.py```

To hook app's URLConf to project, add ```path('<sub_path>/', include('<app>.<route_file>'))``` to ```urlpattern:URLConf```.

Example: ```path('pokemon/', include('pokemon.routes'))```

# Database

We will be using sqlite3

Once schema is changed, run the following commands:
1. ```python manage.py makemigrations``` create snapshots for migration
2. ```python manage.py migrate``` migrate models


# Test

See test files for examples of test cases.

## Note

See ```./pokemon/tests/test_template.py``` for example

## Application Level

1. Replace file ```./<app>/tests.py``` with folder ```./<app>/tests```
2. ```touch ./<app>/tests/__init__.py``` identify as package
3. Test files to prefix with ```test_```

Example ```touch ./<app>/tests/test_models.py```

4. Run tests with ```python manage.py test```, or specific app with ```python manage.py test <app>```

Example ```python manage.py test pokemon```




# Build

No production build

run server in pipenv. specific address may be required i.e `./manage.py runserver "<my_address>:<my_port>"