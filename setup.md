
Reference on how to set up this repo from scratch


# Project
poke_project

# Requirements

python3
pipenv


# Setup

1. in root dir, ```pipenv shell``` will create virtual environment and its config artifacts ```Pipfile``` and ```Pipfile.lock```

After step 1, run commands in virtual environment

2. ```pipenv install django``` install django
3. ```django-admin startproject poke_project .``` start project

4. ```python manage.py runserver``` run server. with some port specified: ```python manage.py runserver 8000```

Step 4. is required if network config is not set in django-admin