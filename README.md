![- Django Rest Framework badge -](https://raw.githubusercontent.com/PascalLefebvre/OC_Project12_EpicEvents/main/badge_drf.svg)
![- PostgreSQL badge -](https://raw.githubusercontent.com/PascalLefebvre/OC_Project12_EpicEvents/main/badge_postgresql.svg)

# Openclassrooms - Project 12 : Develop a secured back-end architecture using Django ORM

    This app is a client relationship management software developed for the Epic Events fictive
    company. This allows it to organize and manage epic parties for its clients.


## Perequisites

* [Python](https://www.python.org/) interpreter
* [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) (to access to the PostgreSQL database service)


## Installation

* After cloning, change into the directory and type :
    
    `python -m venv .venv`

* Next, enter in your virtual environment :
    
    `source .venv/bin/activate` (to deactivate, type `deactivate`)

* Install all the necessary packages :

    `python -m pip install -r requirements.txt`

* Create the ".env" configuration file with a new secret key :

	```
	cp .env.example .env
    python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(f`SECRET_KEY={get_random_secret_key()}`)" >> .env
    ```

* Start up the "postgres15" container in detached mode :

	`sudo docker-compose up -d` (to stop container, type `sudo docker-compose down`)

* Sync the database with Django’s default settings :

    `python manage.py migrate`

* Prepopulate the CRM database after delete the initial database content (to avoid conflicts when loading data) :

	```
	python manage.py shell -c "from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete()"
	python manage.py loaddata crm_db.json
	```

* Start up the local Django web server :

    `python manage.py runserver` (the API should respond with the default address "http://127.0.0.1:8000")


## Access to the front-end interface from the Django Administration

* Go to `http://localhost:8000/admin`

* Log in with `admin` user, password `admin`

* To change a user password from the command line interface :

	`python manage.py changepassword <username>`


## The API documentation

* [Access to the Postman API documentation here](https://documenter.getpostman.com/view/25323756/2s93RZNW2Y)


## Linting

* Type `flake8`

* Open the HTML report located in `./flake_report/index.html` file.


